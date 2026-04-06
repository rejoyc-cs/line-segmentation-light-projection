import cv2
import numpy as np
import os


# -----------------------------
# PREPROCESSING
# -----------------------------
def preprocess(image_path):

    img = cv2.imread(image_path)
    img = cv2.resize(img,(1024,400))

    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bin_img = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,175,55,)
    return gray, bin_img


# -----------------------------
# LIGHT PROJECTION FILLING
# -----------------------------
def light_projection(bin_img, regions=8, fill_value=150):

    h, w = bin_img.shape
    filled = bin_img.copy()

    region_width = w // regions

    for row in range(h):
        # LEFT → RIGHT
        for r in range(regions):

            start = r * region_width
            end = min((r + 1) * region_width, w)

            segment = bin_img[row, start:end]
            obstacle = np.where(segment == 0)[0]

            if obstacle.size > 0:
                stop = obstacle[0]
                filled[row, start:start + stop] = fill_value
            else:
                filled[row, start:end] = fill_value

        # RIGHT → LEFT
        for r in reversed(range(regions)):

            start = r * region_width
            end = min((r + 1) * region_width, w)

            segment = bin_img[row, start:end]

            obstacle = np.where(segment == 0)[0]

            if obstacle.size > 0:
                stop = obstacle[-1]
                filled[row, start + stop:end] = fill_value
            else:
                filled[row, start:end] = fill_value

    return filled

# -----------------------------
# CONNECTED COMPONENT HEIGHT
# -----------------------------
def connected_component_analysis(img):
    heights = []
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    mask = (img != 255).astype(np.uint8) * 255
    contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if w*h < 200:   # remove small noise
            continue
        
        heights.append(h)
        cv2.rectangle(vis, (x,y), (x+w,y+h), (0,0,255), 2)
    
    cc_h_avg = np.mean(heights)
    cc_h_median = np.median(heights)

    return vis, cc_h_avg, cc_h_median

# -----------------------------
# SMOOTHING
# -----------------------------
def smoothing(img, cc_h_avg):
    th_smooth = int(cc_h_avg * 0.15)

    h, w = img.shape
    for col in range(w):
        column_data = img[:, col]
        white_pixels = np.where(column_data == 255)[0]

        if len(white_pixels) == 0:
            continue

        diff = np.diff(white_pixels)
        starts = np.insert(white_pixels[1:][diff != 1], 0, white_pixels[0])
        ends = np.append(white_pixels[:-1][diff != 1], white_pixels[-1])

        for t_start, t_end in zip(starts, ends):
            if t_start == 0 or t_end == h - 1:
                continue

            if img[t_start-1, col] == 0 or img[t_end+1, col] == 0:
                continue

            t_diff = t_end - t_start
            roi = img[t_start:t_end+1, col]

            if t_diff <= th_smooth and (not np.any(roi == 0)):
                mask = (img[t_start:t_end+1, col] != 150)
                img[t_start:t_end+1, col][mask] = 150

    return img

# -----------------------------
# START POINT
# -----------------------------
def detect_start_points(img, cc_h_median):
    h, w = img.shape

    window_height = int(0.25 * cc_h_median)
    density_threshold = 0.05

    start_points = []

    y = 0

    while y + window_height < h:

        window = img[y:y+window_height, :]
        black_pixels = np.sum(window == 0)

        total_pixels = window_height * w
        density = black_pixels / total_pixels

        if density > density_threshold:

            yc = y + window_height // 2
            start_points.append((0, yc))

            # jump to next region
            y += window_height + int(cc_h_median)

        else:
            y += 1

    return start_points

def draw_start_points(img, start_points):
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for x,y in start_points:
        cv2.circle(vis,(x,y),6,(0,0,255),-1)

    return vis

# -----------------------------
# BOUNDARY TRACKING
# -----------------------------
def trace_separator(img, start_point, fill_value=150, max_skip=5):

    h, w = img.shape
    x, y = start_point

    separator = []
    separator.append((x, y))

    while x < w - 1:

        # ---------------------
        # STRAIGHT MOVE
        # ---------------------
        if img[y, x+1] == fill_value:
            x = x + 1
            separator.append((x, y))
            continue

        moved = False

        # ---------------------
        # UPWARD TRACKING
        # ---------------------
        ny = y
        while ny > 1:
            if img[ny-1, x] == fill_value:
                y = ny - 1
                x = x + 1
                separator.append((x, y))
                moved = True
                break
            ny -= 1

        if moved:
            continue

        # ---------------------
        # DOWNWARD TRACKING
        # ---------------------
        ny = y
        while ny < h - 2:
            if img[ny+1, x] == fill_value:
                y = ny + 1
                x = x + 1
                separator.append((x, y))
                moved = True
                break
            ny += 1

        if moved:
            continue

        # ---------------------
        # CUT THROUGH
        # ---------------------
        skip = 0
        while skip < max_skip and x < w-1:
            x += 1
            skip += 1

        separator.append((x, y))

    return separator

def draw_separators(img, separators):

    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for sep in separators:
        for x,y in sep:
            vis[y,x] = (0,0,255)

    return vis

def main(image_path):

    gray, bin_img = preprocess(image_path)

    filled = light_projection(bin_img)

    cv2.imshow("Initial Projection", filled)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    bbox_img, cc_h_avg, cc_h_median = connected_component_analysis(gray)

    cv2.imshow("Bounding Boxes", bbox_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    smoothed = smoothing(filled, cc_h_avg)

    cv2.imshow("After Smooting", bbox_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    start_points = detect_start_points(smoothed, cc_h_median)

    vis = draw_start_points(gray, start_points)

    cv2.imshow("Start Points", vis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    separators = []

    for sp in start_points:
        sep = trace_separator(smoothed, sp)
        separators.append(sep)

    vis = draw_separators(gray, separators)

    cv2.imshow("Separators", vis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #cv2.imshow("Start Points", vis)
    #cv2.waitKey(0)


if __name__ == "__main__":
    filename = "sample.tif"
    main(filename)