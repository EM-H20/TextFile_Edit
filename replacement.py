import os
import re

class FileNumberRemover:
    """
    파일 이름 앞의 숫자를 제거하는 클래스
    """
    def __init__(self):
        # 초기 디렉토리 경로를 None으로 설정
        self.current_path = None
        
    def set_directory(self, directory_path):
        """
        작업할 디렉토리 경로를 설정하는 메서드
        
        매개변수:
            directory_path (str): 설정할 디렉토리 경로
        """
        if os.path.exists(directory_path):
            self.current_path = directory_path
            return True
        return False
    
    def list_txt_files(self):
        """
        현재 디렉토리의 모든 txt 파일 목록을 반환하는 메서드
        """
        if not self.current_path:
            return []
        return [f for f in os.listdir(self.current_path) if f.endswith('.txt')]
    
    def remove_leading_numbers(self, filename):
        """
        파일 이름 앞의 숫자를 제거하는 메서드
        
        매개변수:
            filename (str): 처리할 파일 이름
            
        반환값:
            str: 숫자가 제거된 새 파일 이름
        """
        # 정규표현식을 사용하여 파일 이름 앞의 숫자들을 찾음
        new_name = re.sub(r'^\d+', '', filename)
        
        # 숫자 제거 후 앞에 있는 공백이나 특수문자 제거
        new_name = new_name.lstrip('. _-')
        
        return new_name

    def process_single_file(self, filename):
        """
        단일 파일의 이름에서 숫자를 제거하는 메서드
        """
        try:
            if not self.current_path:
                return "오류: 작업할 디렉토리가 설정되지 않았습니다."
                
            old_path = os.path.join(self.current_path, filename)
            new_name = self.remove_leading_numbers(filename)
            
            # 변경된 것이 없으면 처리하지 않음
            if new_name == filename:
                return f"'{filename}'은(는) 앞에 숫자가 없습니다."
            
            new_path = os.path.join(self.current_path, new_name)
            
            # 파일 이름 변경
            os.rename(old_path, new_path)
            return f"숫자 제거 완료: {filename} → {new_name}"
            
        except Exception as e:
            return f"오류가 발생했습니다: {str(e)}"

    def process_all_files(self):
        """
        모든 txt 파일의 이름에서 숫자를 제거하는 메서드
        """
        files = self.list_txt_files()
        results = []
        
        for filename in files:
            result = self.process_single_file(filename)
            results.append(result)
            
        return results

def main():
    """
    메인 프로그램 실행 함수
    """
    remover = FileNumberRemover()
    
    print("\n=== 파일 이름 앞 숫자 제거 프로그램 ===")
    
    # 작업할 디렉토리 경로 입력 받기
    while True:
        directory = input("\n작업할 디렉토리 경로를 입력하세요: ")
        if remover.set_directory(directory):
            print(f"\n'{directory}' 디렉토리가 설정되었습니다.")
            break
        else:
            print("\n오류: 유효하지 않은 디렉토리 경로입니다. 다시 입력해주세요.")
    
    while True:
        print("\n=== 메뉴 ===")
        print("1. 현재 디렉토리의 TXT 파일 목록 보기")
        print("2. 선택한 파일의 앞 숫자 제거하기")
        print("3. 모든 파일의 앞 숫자 제거하기")
        print("4. 작업 디렉토리 변경하기")
        print("5. 종료")
        
        choice = input("\n원하는 작업을 선택하세요 (1-5): ")
        
        if choice == '1':
            # 현재 디렉토리의 TXT 파일 목록 출력
            files = remover.list_txt_files()
            if files:
                print(f"\n=== {remover.current_path} 의 TXT 파일 목록 ===")
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
            else:
                print("\n현재 디렉토리에 TXT 파일이 없습니다.")
                
        elif choice == '2':
            # 선택한 파일의 앞 숫자 제거
            files = remover.list_txt_files()
            if not files:
                print("\n현재 디렉토리에 TXT 파일이 없습니다.")
                continue
                
            print(f"\n=== {remover.current_path} 의 TXT 파일 목록 ===")
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}")
                
            filename = input("\n숫자를 제거할 파일 이름을 입력하세요: ")
            result = remover.process_single_file(filename)
            print(f"\n{result}")
            
        elif choice == '3':
            # 모든 파일의 앞 숫자 제거
            files = remover.list_txt_files()
            if not files:
                print("\n현재 디렉토리에 TXT 파일이 없습니다.")
                continue
                
            print("\n모든 파일의 앞 숫자를 제거합니다...")
            results = remover.process_all_files()
            print("\n=== 처리 결과 ===")
            for result in results:
                print(result)
            
        elif choice == '4':
            # 작업 디렉토리 변경
            directory = input("\n새로운 디렉토리 경로를 입력하세요: ")
            if remover.set_directory(directory):
                print(f"\n작업 디렉토리가 '{directory}'로 변경되었습니다.")
            else:
                print("\n오류: 유효하지 않은 디렉토리 경로입니다.")
            
        elif choice == '5':
            # 프로그램 종료
            print("\n프로그램을 종료합니다.")
            break
            
        else:
            # 잘못된 입력 처리
            print("\n올바른 선택지를 입력하세요.")

# 프로그램 시작점
if __name__ == "__main__":
    main()