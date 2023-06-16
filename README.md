# 2023 컴파일러 동아리 작업작품
### 부제: AI를 활용한 자동 커리큘럼 제공 및 등급 예측 프로그램

***
## 1. 프로젝트 개요
### 1.1. 프로젝트 목적
- 본 프로젝트는 본격적인 공부를 시작하는 고등학교 1학년 학생들을 위해,<br>예상 등급과, 커리큘럼, 추후에는 희망자에 한해 비슷한 등급의 학생들을 매칭시켜 <br>학습 메이트를 만드는 서비스를 제공하는 것을 목적으로 하는 프로젝트 입니다.
### 1.2. 프로젝트 기능
- 모의고사 문제를 기반으로한 등급 예측 기능
- 등급에 따른 커리큘럼 제공 기능
- 학습 메이트 매칭 기능
- 학습 메이트와의 스터디 기능
- 학습 메이트와의 스터디 기록 기능
- 학습 메이트와의 스터디 결과 공유 기능
### 1.3. 프로젝트 기대효과
- 학생들이 공부를 시작할 때, 어떤 과목을 공부해야 하는지, 어떤 순서로 공부해야 하는지, <br>어떤 등급을 받을 수 있는지 등을 예측하여 학생들이 공부를 시작할 때 도움을 줄 수 있습니다.
- 학생들이 공부를 하면서, 같이 공부할 수 있는 학습 메이트를 만들어 줄 수 있습니다.
***
## 2. 프로젝트 구성
### 2.1. 프로젝트 구조
- 프로젝트는 크게 3가지로 구성되어 있습니다.
  - AI 모델
  - 웹 서버
  - 클라이언트
### 2.2. 프로젝트 구성도
프로젝트는 다음과 같은 구성 요소로 이루어져 있습니다:
1. 3개의 DNN AI 모델과 [OMR 모델](https://github.com/Udayraj123/OMRChecker) or [OMR Mirror1](https://github.com/rbaron/omr): 이 모델들은 각각 TCP 기반의 소켓을 사용하여 서로 통신합니다.
2. RPI 4B: 각 모델은 RPI 4B 한 대씩을 사용합니다.
3. 웹 서버: FastAPI를 사용하여 웹 서버를 구축하였습니다.
4. 클라이언트 앱: 플러터를 사용하여 클라이언트 앱을 개발하였습니다.
5. SBC(Single Board Computer): 모든 장비는 SBC 위에 상주하는 2개의 프로세스를 이용합니다.
6. 자원 할당: 각 프로세스에는 2개의 쓰레드가 할당됩니다.
7. TCP 통신: 각 쓰레드는 램에 모델을 상주시키고, TCP 소켓으로 들어오는 정보를 처리/분석한 후 다시 TCP 소켓을 통해 데이터를 보냅니다.
8. 포트 정보: SBC는 4개의 쓰레드를 가지며, n번 쓰레드는 Recv: 760n, Send: 770n 포트를 사용합니다.
9. 내부 네트워크: 성적 및 개인정보가 사용되는 특성상 외부와 공유되지 않는 VPN을 사용하여<br>내부 네트워크를 구성하였습니다.<br>MasterSBC만 외부 데이터를 받아 VPN 망으로 전송합니다.
10. VPN 망: 10.0.0.1/24의 IP 대역을 사용하며, IP 할당은 다음과 같습니다:
    - MasterSBC: 10.0.0.1 (서버: ServerID[0xFF])
    - AI SBC1 (수학 점수 판독 및 수학 커리큘럼 작성): 10.0.0.2 (클라이언트: ClientID[0xEC])
    - AI SBC2 (국어 점수 판독 및 국어 커리큘럼 작성): 10.0.0.3 (클라이언트: ClientID[0xF5])
    - AI SBC3 (영어 점수 판독 및 영어 커리큘럼 작성): 10.0.0.4 (클라이언트: ClientID[0x1A])
    - OMR SBC (OMR 채점 및 분석): 10.0.0.5 (클라이언트: ClientID[0x23])
11. SBC와 MasterSBC 통신: 각 SBC는 MasterSBC와 통신하기 위해 TCP 소켓 8181번을 사용하며,<br>5초마다 HeartBeat를 보냅니다.
12. HeartBeat 감지: HeartBeat가 30초 동안 3번 이하로 수신되면 해당 SBC는 장애로 간주되고,<br>시스템 관리자에게 메일을 전송합니다.
13. 메인 SBC의 역할: OMR 채점/분석 후, 정보를 각 SBC의 쓰레드에<br>WorkID와 함께 동적으로 Load Balancing하여 전송합니다.
14. 서버에 전송되는 패킷들입니다.
 - Master to AiSBC: Total Length: 23 + DataSize bytes, Packet Structure: [Header(1 byte, ClientID), WorkID(4 bytes), Data Length(2 bytes), Data(Max 65535 bytes), Checksum(16 byte, [SHA256])] as Python Struct Module: `>BLH[Data Length]s16s`
 - AiSBC to Master: Packet Structure: [Header(1 byte, ClientID), WorkID(4 bytes), GradeData(1 bytes), Checksum(16 byte, [SHA256])] as Python Struct Module: `>BLHB16s`
 - HeartBeat: Packet Structure: [Header(1 byte, ClientID), Time(as HHMM to MD5, 16 bytes)] as Python Struct Module: `>BL16s`
 - HeartBeat Response: Packet Structure: [Header(1 byte, ClientID), 0x01] as Python Struct Module: `>BB`
 - OMR Packet: 20문항 오지선다 기준 0000 -> 1번 ~ 0001 -> 2번 ~... Python Struct Module: `>20B`
***
## 3. 프로젝트 구현
### 3.1. 프로젝트 구현 환경
- OS: Raspberry Pi OS Lite (64-bit)
- Hostname: MasterSBC, AiSBC1, AiSBC2, AiSBC3, OMR
- MasterSBC SD Card: 128GB (OMR 스캔본 저장)
- AiSBC1, AiSBC2, AiSBC3, OMR SD Card: 32GB
- VPN: WireGuard
- Language: Python 3.9
- IDE: PyCharm
- AI Framework: TensorFlow 2.12
- Web Framework: FastAPI
- Client Framework: Flutter
- Database: MongoDB
***
## Thanks For Reading😘!
***
OMR - ArUco 사용<br>
ArUco<br>
(XXXX) - 학년 과목 타입<br>
전 학년 각 과목당 4타입 - 3 x 2 x 4 = 24타입<br>
1학년 국어 0~3 수학 4~7<br>
2학년 국어 8~11 수학 12~15 <br>
3학년 국어 16~19 수학 20~23<br>
Ex) 1104 - 1학년 수학 4타입 -> 1학년 수학중 0번<br>
Ex2) 3014 - 3학년 국어 14타입 -> 3학년 국어중 0번<br>
ArUco No = 타입 넘버 앞 두글자 hex + 뒤 두글자 hex
