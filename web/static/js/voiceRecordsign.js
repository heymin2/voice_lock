
$(document).ready(function () {
    const record = document.getElementById('record');
    const stop = document.getElementById('stop');
    const soundClips = document.getElementById('sound-clips');
    const sign = document.getElementById('sign');
    const sign_id = document.getElementById('id');
    const check = document.getElementById('check');

    if (navigator.mediaDevices) {
        var constraints = {
            audio: true
        }

        let chunks = []; // 녹음 데이터 저장하기 위한 변수

        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {
                const mediaRecorder = new MediaRecorder(stream);

                // 녹음 버튼 클릭했을 때
                record.onclick = () => {
                    mediaRecorder.start(); //녹음 시작
                    record.style.background = "red";
                    record.style.color = "black";
                };

                // 정지 버튼 눌렀을 때
                stop.onclick = () => {
                    mediaRecorder.stop(); // 녹음 정지
                    record.style.background = "";
                    record.style.color = "";
                };

                mediaRecorder.onstop = e => {
                    // (1) <audio> 태그 담을 컨테이너 객체 생성
                    const clipcontainer = document.createElement('article');

                    // (2) audio 객체 생성 및 속성 설정
                    const audio = document.createElement('audio');
                    audio.setAttribute('controls', '');

                    // (3) 컨테이너에 audio 연결
                    clipcontainer.appendChild(audio);

                    // <div>에  <audio> 태그 출력
                    // 이전에 녹음할 때 추가한 childNode가 존재한다면 제거하고
                    if (soundClips.hasChildNodes())
                        soundClips.removeChild(soundClips.childNodes[0]);
                    //추가
                    soundClips.appendChild(clipcontainer);

                    // chunks에 저장된 녹음 데이터를  audio 양식으로 설정
                    const blob = new Blob(chunks, {
                        'type': 'audio/mp3 codecs=opus'
                    });

                    // chunks 초기화 (초기화 하지 않으면 녹음 내용이 누적 저장됨)
                    chunks = [];

                    // audio 소스 지정
                    const audioURL = URL.createObjectURL(blob);
                    audio.src = audioURL;

                    const formData2 = new FormData();

                    formData2.append("voice", blob, sign_id.value);

                    // 녹음 들리도록
                    const a = document.createElement('a');

                    // 회원가입 버튼 클릭시 통신
                    check.onclick = () => {
                        fetch("http://127.0.0.1:5000/sign", {
                            method: "POST",
                            cache: 'no-cache',
                            body: formData2
                        })
                        const va = document.getElementById('result');
                        va.innerText = '2차 설정'
                    }
                };

                // 녹음 시작 상태가 되면 chunks에   녹음 데이터 저장
                mediaRecorder.ondataavailable = e => {
                    chunks.push(e.data);
                };

            })
            .catch(err => {
                console.log("오류 발생 : " + err)
            })

        sign.onClick = () => {

        }
    }
});