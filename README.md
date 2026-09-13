
# steam_discount_alarm

### 이 steam_discount_alarm 은 codex 의 도움이 들어갔습니다.
</br>

사용하시기전에 다음 절차를 따라 주십시오.  
아래에 더욱 쉬운 이해를 위한 이미지가 있습니다.
</br>
</br>
```
1. 적당한 폴더에 alarm.py를 다운받아 주십시오. (이 파일만 있는 것을 추천)
2. 21 번 중과 22 번줄의 코드에 게임이름과 그 게임의 스팀주소를 붙여 넣어 주십시오.
3. 작업스케줄러를 실행시킨후 작업만들기를 클릭하여 주십시오.
4. 처음뜨는 창 (일반 메뉴) 에서 이름을 정해 주시고 "사용자가 로그온 할때만 실행" 으로 설정해 주십시오.
5. 트리거 메뉴로 넘어가서 새로만들기를 눌러주십시오.
6. 작업시작을 "로그온 할떄", 지연시간에 체크해 주시고 30초 로 체크해 주십시오
7. cmd 혹은 powershell 을 관리자 권한으로 실행시켜서 "  where pythonw  " 라고 검색 해 주십시오.
8. 나온 경로를 기억하고 있다가 동작 메뉴로 넘어가서 새로만들기를 눌러 주십시오.
9. 프로그램에 나온 경로를 입력하여 주십시오. ( 저는 python 을 기존에 다운 하여서 두번째 경로가 있는데 대부분의 사람들은 첫번째 경로 밖에 없을 것입니다. 무엇으로 하여도 결과에 큰 지장은 없습니다. )
10. 인수 추가 에 다음과 같이 입력하여 주십시오 "C:\Users\~ alarm.py 를 놓은 폴더 경로 주소 ~ \alarm.py"
11. 시작 위치 에 다음과 같이 입력하여 주십시오  C:\Users\~ alarm.py 를 놓은 폴더 경로 주소 ~

 주의! 시작 위치에는 따옴표가 없습니다.

추가 <2026_06_08>

간혹 노트북에서 작동이 되지 아니할 경우 설정 메뉴로 가셔서 "컴퓨터가 AC 전원으로 실행 중인 경우에만 작업 시작" 과 "컴퓨터가 배터리 전원으로 전환되면 중지" 를 모두 체크 해제 하여 주십시오.

```
</br>
</br>

![그림 1](https://github.com/peropero1111/steam_discount_alarm/blob/main/img/2026-06-06%20220311%20(1).png) 
</br>
</br>
<img src="https://github.com/peropero1111/steam_discount_alarm/blob/main/img/2026-06-06%20221706.png" width="450" height="450"/>  
</br>
</br>
![](https://github.com/peropero1111/steam_discount_alarm/blob/main/img/2026-06-06%20222142.png)
</br>
</br>
![](https://github.com/peropero1111/steam_discount_alarm/blob/main/img/2026-06-06%20222246.png)
</br>
</br>
![](https://github.com/peropero1111/steam_discount_alarm/blob/main/img/2026-06-06%20222759.png)
</br>
</br>
![](https://github.com/peropero1111/steam_discount_alarm/blob/main/img/2026-06-06%20222357.png)
</br>
</br>
![](https://github.com/peropero1111/steam_discount_alarm/blob/main/img/2026-06-06%20222643.png)
</br>
</br>
추가 <2026_06_08>
</br>
</br>
<img src="https://github.com/peropero1111/steam_discount_alarm/blob/main/img/2026-06-08%20122117.png" width="450" height="450"/>  

- - -

## 면책조항

이 소프트웨어는 어떠한 종류의 명시적 또는 묵시적 보증 없이
**"있는 그대로(AS IS)"** 제공됩니다.

이 프로그램은 Steam에서 제공되는 게임 가격 및 할인 정보를 확인하여
사용자에게 알리는 보조 도구입니다.

프로젝트 작성자는 다음 사항을 보장하지 않습니다.

* Steam에서 제공되는 가격 또는 할인 정보가 항상 정확하거나 최신인 것
* 모든 지역, 통화, 번들 및 프로모션의 가격이 정확하게 처리되는 것
* Steam의 API 또는 기타 서비스가 항상 사용 가능한 것
* 할인 알림이 항상 성공적으로 표시되는 것

Steam의 가격, 할인율 및 구매 가능 여부는 지역, 계정 상태, 세금,
프로모션 및 게시자의 결정 등에 따라 달라질 수 있습니다.

게임을 구매하기 전에는 반드시 Steam의 공식 상점 페이지에서 실제 가격,
할인 조건 및 구매 가능 여부를 직접 확인하는 것을 권장합니다.

이 소프트웨어의 사용 또는 사용 불가능으로 인해 발생하는 손해에 대한
책임은 저장소의 `LICENSE`에 규정된 범위 내에서 제한됩니다.
