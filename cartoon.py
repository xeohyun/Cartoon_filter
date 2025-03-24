import cv2
import numpy as np

def generate_edge_mask(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        7, 5
    )
    return edges

def reduce_color_palette(image, k):
    data = np.float32(image).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.01)
    _, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(image.shape)
    return result

def emphasize_dark_regions(image, threshold=100, factor=0.8):
    image_float = image.astype(np.float32)
    result = np.where(image_float < threshold, image_float * factor, image_float)
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result

def combine_cartoon_image(edges, quantized):
    cartoon = cv2.bitwise_and(quantized, quantized, mask=edges)
    return cartoon

def apply_blur_filter(image):
    blurred = cv2.bilateralFilter(image, 3, 50, 50)
    return blurred

def create_cartoon_image(image):
    edges = generate_edge_mask(image)
    quantized = reduce_color_palette(image, 15)
    quantized = emphasize_dark_regions(quantized, threshold=100, factor=0.8)
    cartoon = combine_cartoon_image(edges, quantized)
    final_cartoon = apply_blur_filter(cartoon)
    return final_cartoon

# 예시용 main 함수
if __name__ == "__main__":
    image_bgr = cv2.imread("img3.jpg")
    if image_bgr is None:
        print("Failed to load image.")
        exit()
    
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    cartoon_image = create_cartoon_image(image_rgb)

    # 필터 결과만 보기 (OpenCV로 띄우기)
    cartoon_bgr = cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR)


   # 원본 + 결과 이미지 hstack
    combined = cv2.hconcat([image_bgr, cartoon_bgr])
    
    # 화면 출력
    cv2.imshow("Original vs Cartoon", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
