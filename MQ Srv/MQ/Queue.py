class Queue:
    def __init__(self):
        self._to_omr = []
        self._to_ai1 = []
        self._to_ai2 = []
        self._to_mst = []

    def enqueue(self, item, to):
        if to == "OMR":
            self._to_omr.append(item)
        elif to == "AI1":
            self._to_ai1.append(item)
        elif to == "AI2":
            self._to_ai2.append(item)
        elif to == "MST":
            self._to_mst.append(item)
        else:
            raise ValueError("Invalid to value")

    def dequeue(self, to):
        if to == "OMR":
            return self._to_omr.pop(0)
        elif to == "AI1":
            return self._to_ai1.pop(0)
        elif to == "AI2":
            return self._to_ai2.pop(0)
        elif to == "MST":
            return self._to_mst.pop(0)
        else:
            raise ValueError("Invalid to value")

    def peek(self, to):
        if to == "OMR":
            return self._to_omr[0]
        elif to == "AI1":
            return self._to_ai1[0]
        elif to == "AI2":
            return self._to_ai2[0]
        elif to == "MST":
            return self._to_mst[0]
        else:
            raise ValueError("Invalid to value")

    def is_empty(self, to):
        if to == "OMR":
            return len(self._to_omr) == 0
        elif to == "AI1":
            return len(self._to_ai1) == 0
        elif to == "AI2":
            return len(self._to_ai2) == 0
        elif to == "MST":
            return len(self._to_mst) == 0
        else:
            raise ValueError("Invalid to value")

    def size(self, to):
        if to == "OMR":
            return len(self._to_omr)
        elif to == "AI1":
            return len(self._to_ai1)
        elif to == "AI2":
            return len(self._to_ai2)
        elif to == "MST":
            return len(self._to_mst)
        else:
            raise ValueError("Invalid to value")

    def get_all(self):
        return {
            "OMR": self._to_omr,
            "AI1": self._to_ai1,
            "AI2": self._to_ai2,
            "MST": self._to_mst
        }
