# DevRQ(Requirements)
***
![Flowchart](https://cdn.discordapp.com/attachments/990941443830976554/1125812974737698816/wsNUAAAAASUVORK5CYII.png)
***
모든 항목은 4W-1H를 기반으로 작성합니다.
- What: 무엇을 다루는 모듈인가?
- Why: 왜 이 모듈이 사용하는가?
- When: 언제 사용하는가?
- Where: 어디서 사용하는가?
- How: 어떻게 사용하는가?
***
## Service Structure
- Module
    - [OMR](#omr)
    - [AruCo](#aruco)
    - [Message Queuing](#message-queuing)
    - [Hardware](#hardware)
    - [Web(Admin Page)](#web-admin-page)
    - [Web(Client Page)](#web-client-page)
***
# OMR
* 4W-1H
    - What: OMR은 Optical Mark Recognition의 약자로 광학식 마크 인식
    - Why: OMR은 시험지의 답안을 인식하기 위해 사용
    - When: 시험지의 답안을 인식할 때 사용
    - Where: 마스터에서 보낸 내용을 OMR SERVER가 처리할때 사용
    - How: 마스터 -> 패킷 -> Message Queuing -> OMR SERVER -> 패킷 -> 마스터
***
# AruCo
* 4W-1H
    - What: AruCo는 4x4의 내부 픽셀로 이루어진 흑/백 마커
    - Why: AruCo는 시험지의 종류를 인식할때 사용
    - When: 시험지 인식 후 시험지의 종류를 인식할 때 사용
    - Where: 마스터에서 보낸 내용을 AruCo SERVER가 처리할때 사용
    - How: 마스터 -> 패킷 -> Message Queuing -> AruCo SERVER -> 패킷 -> 마스터
***
# Message Queuing
* 4W-1H
    - What: Message Queuing은 메시지를 큐에 저장하는 것
    - Why: Message Queuing은 OMR, AruCo, Hardware, Web(Admin Page), Web(Client Page)가 사용하는 메시지(패킷)를 저장하기 위해 사용
    - When: OMR, AruCo, Hardware, Web(Admin Page), Web(Client Page)가 메시지(패킷)를 생성/사용할 때 사용
    - Where: 마스터 SBC에서 독립적 프로세스로 사용
    - How: OMR, AruCo, Hardware, Web(Admin Page), Web(Client Page) -> 패킷 -> Message Queuing -> OMR, AruCo, Hardware, Web(Admin Page), Web(Client Page) (필요한 EndPoint가 Receive하면서 처리)
***
# Hardware
4W-1H 예외
동작 여부의 GreenLED + 오류 여부의 RedLED(EndPoints)
Master -> OLED + YellowLED(동작 여부) + GreenLED(동작 여부)
Master의 YLED와 GLED는 번갈아 가면서 점멸
If Not 마스터 SBC 동작 오류 
***
# Web(Admin Page)
[**추가예정**]
MQSrv의 실시간 큐 / 각 서버의 쓰레드로 간 Work의 통계 / 작업량
***
# Web(Client Page)
[**추가예정**]