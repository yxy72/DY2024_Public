"""DY_Server_Py URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views as v

# 静态资源相关
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('cnmf/',v.cnm),
    path('dev/',v.dev),


    path('login/',v.loginView),
    path('getuser/',v.getUserView),
    
    path('logout/',v.logout),
    path('register/',v.register),
    path('regist/config/',v.registConfig),
    path('checkauth/',v.checkauth),

    path('getalluser/',v.getAllUser),
    path('changeuser/',v.changeUser),
    path('deleteuser/',v.deleteUser),
    path('postuseravatar/',v.postUserAvatar),


    path('config/setKGIP/',v.setKGIPView),



    path('optimize/',v.optimizeView),
    path('train/layers/',v.calModelLayer),
    path('train/',v.train),
    # path('train/save/',v.trainSaveView),

    path('querymodel/',v.queryModelInfo),
    path('predict/',v.predictView),
    path('postmodel/',v.postModelView),
    
    path('predict/data/',v.predictDataView),

    path('embed/',v.embedView),
    

    path('kg/init/',v.kgInitView),
    path('kg/query/',v.kgQueryView),
    path('kg/export/',v.kgExportView),
    path('kg/send/',v.kgSendView),
    

    path('hardcnt/',v.fakeView),
    
    path('analyze/train/',v.analyzeTrainView),
    path('analyze/predict/',v.analyzePredictView),
    path('analyze/get/',v.getAnalyzeView),


    path('quality/getItems/',v.QM_GET_ITEMS_VIEW),
    path('quality/getChart/',v.QM_GET_CHART_VIEW),





    # 运维接口
    path('option/RegisCode/',v.RegisCodeView),
    path('option/TokenExpires/',v.TokenExpiresView),
    path('option/GraphTime/',v.GraphTimeView),
    path('option/ClearLogin/',v.ClearLoginView),
    path('option/isSubsystem/',v.IsSubsystemView),
    path('quality/postModel/',v.QM_POST_MODEL_VIEW),
    path('quality/delModel/',v.QM_DELETE_MODEL_VIEW),
    path('quality/postData/',v.QM_POST_DATA_VIEW),
    



    # 数据接口
    path('cause/',v.ErrorCauseView),




] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

