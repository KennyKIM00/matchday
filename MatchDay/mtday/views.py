from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Clubs, User

from django.contrib.auth.decorators import login_required  # 로그인 상태 확인
from django.contrib.auth import logout


# 내 정보 페이지
@login_required(login_url="login")  # 로그인하지 않으면 로그인 페이지로 리다이렉트
def my_info_view(request):
    user_id = request.session.get("user_id")
    user = User.objects.get(id=user_id)
    return render(request, "my_info.html", {"user": user})

# 로그아웃
def logout_view(request):
    logout(request)  # 세션 정보 삭제
    return redirect("home")  # 로그아웃 후 로그인 페이지로 이동





def home(request):
    # GET 요청에서 'ctprvn_nm', 'signgu_nm', 'item_nm' 값을 가져옴
    ctprvn_nm = request.GET.get('ctprvn_nm') or request.session.get('city')  # 시도명: GET 또는 세션 값
    signgu_nm = request.GET.get('signgu_nm') or request.session.get('district')  # 시군구명: GET 또는 세션 값
    item_nm = request.GET.get('item_nm')
    
    # 초기화된 queryset: 필터링 안 한 전체 데이터
    clubs = Clubs.objects.all()

    # 만약 검색어가 입력되면 해당 필드로 필터링
    if ctprvn_nm:
        clubs = clubs.filter(ctprvn_nm__icontains=ctprvn_nm)  # 시도명 필터
    if signgu_nm:
        clubs = clubs.filter(signgu_nm__icontains=signgu_nm)  # 시군구명 필터
    if item_nm:
        clubs = clubs.filter(item_nm=item_nm)  # 종목명 정확히 일치 필터

    # 모든 종목명 가져오기 (중복 제거)
    sports = Clubs.objects.values_list('item_nm', flat=True).distinct().order_by('item_nm')
    
    return render(request, 'home.html', {
        'clubs': clubs,
        'sports': sports
    })
    
    
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        print("입력된 username:", username)
        print("입력된 password:", password)

        # 데이터베이스에서 유저 검증
        try:
            user = User.objects.get(username=username, password=password)
            print("로그인 성공: ", user)
            # 세션 설정
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            request.session["city"] = user.city  # 시도명
            request.session["district"] = user.district
            
            messages.success(request, "로그인에 성공했습니다.")
            return redirect("home")  # 로그인 성공 시 홈 페이지로 리디렉션
        except User.DoesNotExist:
            print("로그인 실패: 아이디 또는 비밀번호가 잘못되었습니다.")
            messages.error(request, "아이디 또는 비밀번호가 잘못되었습니다.")
    
    return render(request, "login.html")


def sign_up_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        email = request.POST.get('email')
        city = request.POST.get('region')  # 'region'과 'district'는 템플릿의 select input 이름과 일치해야 함
        district = request.POST.get('district')
        if User.objects.filter(username=username).exists():
            return render(request, 'sign_up.html', {
                'error': '이미 사용 중인 아이디입니다.'
            })

        try:
            user = User.objects.create(
                username=username,
                password=password,
                name=name,
                birth_date=birth_date,
                email=email,
                city=city,
                district=district
            )
            return redirect('login')  # 로그인 페이지로 리디렉션
        except IntegrityError:
            return render(request, 'sign_up.html', {
                'error': '회원가입 중 오류가 발생했습니다. 다시 시도해주세요.'
            })

        return redirect('login')  # 가입 후 로그인 페이지로 리디렉션

    return render(request, 'sign_up.html')

