import os
from datetime import datetime

class BibleReader:
    """
    성경 읽기를 위한 클래스
    성경 내용을 저장하고 관리하는 기능을 제공합니다.
    """
    def __init__(self):
        # 현재 읽고 있는 위치를 저장하는 변수들
        self.current_book = ""        # 현재 책
        self.current_chapter = 1      # 현재 장
        self.current_verse = 1        # 현재 절
        self.bible_content = {}       # 성경 전체 내용을 저장할 딕셔너리
        
    def load_bible(self, filename):
        """
        성경 텍스트 파일을 읽어오는 메소드
        
        Args:
            filename (str): 성경 텍스트 파일의 경로
            
        Returns:
            bool: 파일 로드 성공 여부
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                current_book = ""      # 현재 처리 중인 책
                current_chapter = 0    # 현재 처리 중인 장
                
                # 파일의 각 줄을 순회하며 처리
                for line in file:
                    line = line.strip()    # 줄 끝의 공백 제거
                    if not line:           # 빈 줄은 건너뛰기
                        continue
                        
                    # 새로운 책의 시작 확인 (예: "창세기", "출애굽기" 등)
                    # 숫자가 없고 길이가 짧은 줄은 책 제목으로 간주
                    if not any(char.isdigit() for char in line) and len(line) < 10:
                        current_book = line
                        self.bible_content[current_book] = {}
                        current_chapter = 0
                    
                    # 장 구분 확인 (예: "제1장")
                    elif line.startswith('제') and '장' in line:
                        current_chapter = int(''.join(filter(str.isdigit, line)))
                        self.bible_content[current_book][current_chapter] = {}
                    
                    # 절 내용 저장 (예: "1 태초에...")
                    elif line[0].isdigit():
                        # 절 번호와 내용을 분리
                        verse_num = int(''.join(filter(str.isdigit, line.split()[0])))
                        verse_text = ' '.join(line.split()[1:])
                        self.bible_content[current_book][current_chapter][verse_num] = verse_text
                        
            return True
        except FileNotFoundError:
            print(f"Error: {filename} 파일을 찾을 수 없습니다.")
            return False
        except Exception as e:
            print(f"Error: 파일을 읽는 중 오류가 발생했습니다. {str(e)}")
            return False

    def display_verse(self, book, chapter, verse):
        """
        지정된 구절을 화면에 표시하는 메소드
        
        Args:
            book (str): 책 이름
            chapter (int): 장 번호
            verse (int): 절 번호
            
        Returns:
            bool: 구절 표시 성공 여부
        """
        try:
            verse_text = self.bible_content[book][chapter][verse]
            print(f"\n{book} {chapter}장 {verse}절:")
            print(verse_text)
            return True
        except KeyError:
            print("해당 구절을 찾을 수 없습니다.")
            return False

    def save_reading_progress(self):
        """
        현재 읽은 위치를 파일에 저장하는 메소드
        현재 책, 장, 절 정보와 저장 시간을 함께 기록합니다.
        """
        with open('bible_progress.txt', 'w', encoding='utf-8') as f:
            f.write(f"{self.current_book},{self.current_chapter},{self.current_verse}")
            f.write(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def load_reading_progress(self):
        """
        이전에 저장한 읽은 위치를 불러오는 메소드
        
        Returns:
            bool: 진행 상황 불러오기 성공 여부
        """
        try:
            with open('bible_progress.txt', 'r', encoding='utf-8') as f:
                data = f.readline().strip().split(',')
                self.current_book = data[0]
                self.current_chapter = int(data[1])
                self.current_verse = int(data[2])
                return True
        except FileNotFoundError:
            return False

def main():
    """
    메인 프로그램 실행 함수
    사용자 인터페이스를 제공하고 사용자 입력을 처리합니다.
    """
    # BibleReader 인스턴스 생성
    reader = BibleReader()
    
    # 성경 텍스트 파일 로드
    if not reader.load_bible('C:\Users\루카우카\Desktop\개역개정-pdf, txt\개역개정-text - 복사본'):
        return
    
    # 이전 읽은 위치 불러오기
    if reader.load_reading_progress():
        print(f"마지막으로 읽은 위치: {reader.current_book} {reader.current_chapter}장 {reader.current_verse}절")
    
    # 메인 프로그램 루프
    while True:
        print("\n=== 성경 읽기 프로그램 ===")
        print("1. 특정 구절 읽기")
        print("2. 다음 구절 읽기")
        print("3. 현재 위치 저장")
        print("4. 종료")
        
        choice = input("\n선택하세요 (1-4): ")
        
        # 1. 특정 구절 읽기
        if choice == '1':
            book = input("책 이름을 입력하세요 (예: 창세기): ")
            chapter = int(input("장을 입력하세요: "))
            verse = int(input("절을 입력하세요: "))
            
            # 구절을 표시하고 현재 위치 업데이트
            if reader.display_verse(book, chapter, verse):
                reader.current_book = book
                reader.current_chapter = chapter
                reader.current_verse = verse
                
        # 2. 다음 구절 읽기
        elif choice == '2':
            # 현재 장의 전체 절 수 확인
            current_verses = len(reader.bible_content[reader.current_book][reader.current_chapter])
            
            # 현재 장에서 다음 절이 있는 경우
            if reader.current_verse < current_verses:
                reader.current_verse += 1
            else:
                # 다음 장으로 이동
                max_chapters = len(reader.bible_content[reader.current_book])
                if reader.current_chapter < max_chapters:
                    reader.current_chapter += 1
                    reader.current_verse = 1
                else:
                    print("현재 책의 마지막 구절입니다.")
                    continue
                    
            reader.display_verse(reader.current_book, reader.current_chapter, reader.current_verse)
            
        # 3. 현재 위치 저장
        elif choice == '3':
            reader.save_reading_progress()
            print("현재 위치가 저장되었습니다.")
            
        # 4. 프로그램 종료
        elif choice == '4':
            print("프로그램을 종료합니다.")
            break
            
        # 잘못된 입력 처리
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")

# 프로그램 시작점
if __name__ == "__main__":
    main()