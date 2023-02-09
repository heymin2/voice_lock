# 목소리 로그인
목소리를 음성 인식 후 이미지화한 후 샴네트워크를 이용하여 학습 및 추론

## 기능
### 🔉녹음
1. static/js/voiceRecord.js (로그인용)
2. static/js/voiceRecordsign.js (회원가입용)


자바스크립트 MediaRecorder 기능으로 녹음


확인 버튼 클릭시 FormData에 blob 형태로 저장 -> 파일 전송


### 💿 변환
app.py -> sign_file(), login_file()


wav 파일을 이미지로 변환시킴


wav plot, MFCC 두 가지로 변환 가능

### ✏️ 학습
siamese.py -> train()


회원가입 완료시 작동


변환을 통해 train 폴더에 id명으로 저장 - 라벨 이름 


학습 완료시 siamese.pt로 학습 모델 저장


### 📝 추론
siamese.py -> test()

로그인 완료시 작동


변환을 통해 test 폴더에 id명으로 저장 - 라벨 이름


siamese.pt 이용하여 test 폴더와 train 폴더 비교


성공, 실패 기준: 현재 로그인 하려는 id와 가장 유사한 라벨이 동일한가

로그인 성공시 page로 넘어감
로그인 실패시 로그인 실패!! 뜸








## 실행
```
python3 app.py
```
 
 [참조 자료](https://metar.tistory.com/entry/%EC%BD%94%EB%9E%A9%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%83%B4-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC-%EA%B5%AC%ED%98%84)
