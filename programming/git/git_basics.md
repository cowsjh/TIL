**디렉 토리** *-add->* **스테이징** *-commit->* **로컬 저장소(.git)** *-push->* **원격 저장소(repo)**

> **WARNING — 현재 브랜치 위치를 항상 확인**
> `merge`·`rebase`·`push`는 모두 "지금 어느 브랜치에 서 있느냐"를 기준으로 동작한다. `git status` / `git branch`로 위치부터 확인.


**알면 좋은 커밋 메세지**

| 접두어       | 의미                      |
| --------- | ----------------------- |
| `Feat:`   | 새 기능 추가                 |
| `Fix:`    | 버그 수정                   |
| `Test:`   | 테스트 추가/수정               |
| `Design:` | 설계 변경                   |
| `Style:`  | 코드 스타일(포맷팅 등, 로직 변경 없음) |
| `Docs:`   | 문서 수정                   |

## 기초

```bash
git clone 주소 #최초 1회

git status
git diff
git add .
git commint -m ""
git push
git pull

git log
```

## 브랜치

```bash
git branch # 로컬 브랜치 목록
git branch -a # 로컬 + 원격 브랜치 전부
git branch -v # 마지막 커밋과 함께 보기

git branch 브랜치이름 # 새 브랜치 생성
git switch 브랜치
git switch -c 브랜치 #생성 + 이동

git branch -d 브랜치 #병합돤 브랜치 삭제
git branch -D 브랜치 #   강제 삭제

git push origin 브랜치 # 브랜치 push
git push -u origin 브랜치 # push + 업스트림 연결
git log --oneline --gragh # 브랜치 시각화

git merge 브랜치 #병합 받을 브랜치로 이동 후 실행

git branch -r #모든 깃에 브런치들 (원격에 있는거 까지)
git switch -t origin/브런치 #원격 브런치 가져오기
```

### 삭제

```bash
git branch -D <브랜치> #로컬 에서만 삭제 (병합되지 않은 경우)
git branch -d <브랜치> #(병합된 경우)
git push origin --delete <브랜치> #원격 삭제
```

## 수정

```bash
git restore 파일 # 디렉터리 수정을 버린다.
git restore --staged 파일 # 스테이징에서 뺀다
git revert 커밋ID #반대 변경을 새커밋으로 추가
```

## remote
```bash
git remote add origin <URL>
```

## 커밋 메세지

| 접두어       | 의미                      |
| --------- | ----------------------- |
| `Feat:`   | 새 기능 추가                 |
| `Fix:`    | 버그 수정                   |
| `Test:`   | 테스트 추가/수정               |
| `Design:` | 설계 변경                   |
| `Style:`  | 코드 스타일(포맷팅 등, 로직 변경 없음) |
| `Docs:`   | 문서 수정                   |

---

git 명령어는 [[linux 기본 명령어]] 셸 환경 위에서 실행된다.
