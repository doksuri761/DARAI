import cv2


def ArUco(imgPath):
    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    }

    aruco_type = "DICT_4X4_50"
    ArUco_OMRNo = {0: '0B04', 1: '0B05', 2: '0B06', 3: '0B07', 4: '150C', 5: '150D', 6: '150E', 7: '150F', 8: '1F14',
                   9: '1F15', 10: '1F16', 11: '1F17', 12: '0A00', 13: '0A01', 14: '0A02', 15: '0A03', 16: '1408',
                   17: '1409', 18: '140A', 19: '140B', 20: '1E10', 21: '1E11', 22: '1E12', 23: '1E13'}

    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])
    arucoParams = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, arucoParams)

    img = cv2.imread(imgPath, cv2.IMREAD_ANYCOLOR)
    h, w, _ = img.shape

    width = 1000
    height = int(width * (h / w))
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

    corners, ids, rejected = detector.detectMarkers(img)
    return ArUco_OMRNo[ids[0][0]]


if __name__ == '__main__':
    import src.entry
    import pathlib

    print(src.entry.entry_point(pathlib.Path("./DARAIOMR001.jpg"), "D:\dong-a-ri-AI\OMRChecker\inputs"))
    print(ArUco("./OMR/DARAIOMR001.jpg"))
