"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from superadmin import super_views
from apiapp import views,pi_views
from virtualExpert import pm_views,hm_views,sm_views,am_views,ad_pro_views,ad_dis_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signup),
    path("otp/<id>",views.otp),
    path('signin/',views.signin),
    path('profileidcard/<uid>',views.profileIdCard),
    path('profileform/<id>',views.profileForm),
    path('profilepicture/<id>',views.profilePicture),
    path('primarydetails/<id>',views.primaryDetails),
    path('familydetails/<id>',views.familyDetails),
    path('contactdetails/<id>',views.contactDetails),
    path("alldata/<id>",views.getAllUserData),
    path("about_candidate/<id>",views.about_candidate),
    path("alluserdata/",views.alldata),
    path("all_female_user_data/<id>",views.all_female_user_data),
    path("all_male_user_data/<id>",views.all_male_user_data),
    path('requested_list/<id>',views.requested_list),
    path('received_list/<id>',views.received_list),
    path('block/<id>',views.block),
    path('pf_coin/<id>',views.pf_coin),

    #favorites
    path('favorites/<id>',views.favorites),
    path('favorites_to_me/<id>',views.favorites_to_me),
    #saved search
    path('saved_search/<id>',views.saved_search),
    #happycouples
    path('happy_couples/<id>',views.happy_couples),
    path('happy_couples_all/',views.happy_couples_all),
    path('happy_couples_one/<id>',views.happy_couples_one),
    #my-investigator
    path('my_investigator/<id>',views.my_investigator),
    #question and answer
    path('my_question_and_answer/<id>',views.my_question_and_Answer),
    #ratings and feedback
    path('ratings_feedback/<id>',views.ratings_feedback),
    #my manager
    path('my_manager/<id>',views.my_manager),
    #complaints and replay
    path('my_complaints/<id>',views.my_complaints),
    
    # profile_finder_highlights
    path('ads_highlight/<id>',views.ads_highlight),

    # distributor ads list 
    path('all_provider_ads/',views.adprovider_ads),
    path('all_distributor_ads/',views.addistributor_ads),
    path('proads_views_count/<id>',views.proads_views_count),
    path('disads_views_count/<id>',views.disads_views_count),
    path('ads_viewed_data/<id>',views.ads_viewed_data),
    path('ads_viewed_details/<id>',views.ads_viewed_details),

    #password reset
    path('profilefinder_password_reset/<id>',views.password_reset),
    path('pass_profilefinder_update/<id>',views.pass_profilefinder_update),

    # forgetpassword
    path('pf_forget_password/',views.pf_forget_password),
    path('pf_forget_password_otp/<id>',views.pf_forget_password_otp),



#superadmin
    
    path('superadmin/signin/',super_views.signin),
    path('superadmin/my_data/<id>',super_views.my_data),
    path('superadmin/emra_coin/<id>',super_views.emra_coin_add),
    path('superadmin/external_expenses_add/<id>',super_views.external_expenses_add),
    path('superadmin/public_user_delete/<id>',super_views.public_user_delete),
    path('superadmin/hirirng_user_delete/<id>',super_views.hirirng_user_delete),
    path('superadmin/profile_user_delete/<id>',super_views.profile_user_delete),
    path('superadmin/sales_user_delete/<id>',super_views.sales_user_delete),
    path('superadmin/pi_user_delete/<id>',super_views.pi_user_delete),
    path('superadmin/adpro_user_delete/<id>',super_views.adpro_user_delete),
    path('superadmin/addis_user_delete/<id>',super_views.addis_user_delete),
    path('superadmin/subscription/<id>',super_views.subscriptionN),
    path('superadmin/single_subscriptionN/<id>/<sid>',super_views.single_subscriptionN),
    path('superadmin/commision/<id>',super_views.commisionn),
    path('superadmin/single_commisionn/<id>',super_views.single_commisionn),
    path('superadmin/third_party_userrr/<id>',super_views.third_party_userrr),
    path('superadmin/single_third_party_userrr/<id>',super_views.single_third_party_userrr),
    path('superadmin/all_complaint_list/<id>',super_views.all_complaint_list),
    path('superadmin/incentive_settings/<id>',super_views.incentive_settingss),  



    


#///////////private investigator///////////////////
    path('pi_signup/',pi_views.signup),
    path("pi_otp/<id>",pi_views.otp),
    path('pi_signin/',pi_views.signin),
    path('pi_profilePicture/<id>',pi_views.profilePicture),
    path('pi_complete_account/<id>',pi_views.pi_complete_account),
    path('pi_edit_account/<id>',pi_views.pi_edit_account),
    path("all_private_investigator_data",pi_views.all_pi_data),
    path("pi_my_data/<id>",pi_views.pi_my_data),
    path("pi_my_clients/<id>",pi_views.my_clients),
    path("total_ratings/<id>",pi_views.total_ratings),
    # pass reset
    path("privateinvest_password_reset/<id>",pi_views.password_reset),
    path('pass_privateInvestigator_update/<id>',pi_views.pass_privateInvestigator_update),
    path('pi_email_update/<id>',pi_views.pi_email_update),
    # forget password
    path('pi_forget_password/',pi_views.pi_forget_password),
    path('pi_forget_password_otp/<id>',pi_views.pi_forget_password_otp),





#//////////profile manager///////////
    path('pm_myid/<id>',pm_views.pm_myid),
    path('pm_signup/',pm_views.pm_signup),
    path("pm_signin/",pm_views.pm_signin),
    path("pm_otp/<id>",pm_views.pm_otp),
    path("pm_profile_picture/<id>",pm_views.pm_profile_picture),
    path("pm_complete_account/<id>",pm_views.pm_complete_account),
    path("pm_edit_account/<id>",pm_views.pm_edit_account),
    path("all_pm_data/",pm_views.all_pm_data),
    path("pm_my_data/<id>",pm_views.pm_my_data),
    path("pm_my_clients/<id>",pm_views.my_clients),
    #status
    path("status/<id>",pm_views.pf_status),
    #users
    path("add_user/<id>",pm_views.add_user),
    path("pm_my_users_data/<id>",pm_views.my_users_data),
    path("single_users_data/<id>",pm_views.single_users_data),
    # email reset
    path('pm_email_update/<id>',pm_views.pm_email_update),
    # password reset
    path('pm_password_update/<id>',pm_views.pm_password_update),
    path('pm_password_reset/<id>',pm_views.pm_password_reset),
    # Forget password
    path('pm_forget_password/',pm_views.pm_forget_password),
    path('pm_forget_password_otp/<id>',pm_views.pm_forget_password_otp),
    
    

    


    



#//////////hiring manager///////////
    path('hm_signup/',hm_views.hm_signup),
    path("hm_otp/<id>",hm_views.hm_otp),
    path("hm_signin/",hm_views.hm_signin),
    path("hm_profile_picture/<id>",hm_views.hm_profile_picture),
    path("hm_upload_account/<id>",hm_views.hm_upload_account),
    path("hm_edit_account/<id>",hm_views.hm_edit_account),
    path("hm_my_data/<id>",hm_views.hm_my_data),
    path("all_hm_data/",hm_views.all_hm_data),
    path("profile_manager_upload_account/<id>",hm_views.profile_manager_upload_account),
    path("ad_provider_upload_account/<id>",hm_views.ad_provider_upload_account),
    path("ad_distributor_upload_account/<id>",hm_views.ad_distributor_upload_account),
    path("sales_upload_account/<id>",hm_views.sales_upload_account),
    path("hiring_upload_account/<id>",hm_views.hiring_upload_account),
    path("affiliate_upload_account/<id>",hm_views.affiliate_upload_account),
    path("private_investigator_upload_account/<id>",hm_views.private_investigator_upload_account),

    path("add_user/<id>",hm_views.add_user),
    path("hm_my_users_data/<id>",hm_views.my_users_data),
    path("single_users_data/<id>",hm_views.single_users_data),

    path('hm_email_update/<id>',hm_views.hm_email_update),
    path('hm_password_reset/<id>',hm_views.hm_password_reset),
    path('hm_password_update/<id>',hm_views.hm_password_update),
    
    path('hm_forget_password/',hm_views.hm_forget_password),
    path('hm_forget_password_otp/<id>',hm_views.hm_forget_password_otp),
    


#//////////sales manager///////////
    path('sm_signup/',sm_views.sm_signup),
    path("sm_otp/<id>",sm_views.sm_otp),
    path("sm_signin/",sm_views.sm_signin),
    path("sm_profile_picture/<id>",sm_views.sm_profile_picture),
    path("sm_upload_account/<id>",sm_views.sm_upload_account),
    path("all_sm_data/",sm_views.all_sm_data),
    path("sm_my_data/<id>",sm_views.sm_my_data),
    path("sm_edit_data/<id>",sm_views.sm_edit_data),
    path("sm_email_update/<id>",sm_views.sm_email_update),
    path("password_reset/<id>",sm_views.password_reset),
    path("pass_sales_update/<id>",sm_views.pass_sales_update),
    path("sm_add_user/<id>",sm_views.add_user),
    path("sm_my_users_data/<id>",sm_views.my_users_data),
    path("single_users_data/<id>",sm_views.single_users_data),
    path('sales_forget_password/',sm_views.sales_forget_password),
    path('sales_forget_password_otp/<id>',sm_views.sales_forget_password_otp),
    
    # ad_pro_ads
    path("adprovider_ads/",sm_views.adprovider_ads),
    path("ad_pro_list/",sm_views.ad_pro_list),
    path("view_adpro_id/<id>",sm_views.view_adpro_id),
    path("addpro_ads_id/<id>",sm_views.addpro_ads_id),
    path("adspro_status_active/<id>",sm_views.adspro_status_active),
    path("adspro_status_reject/<id>",sm_views.adspro_status_reject),
    # ad_dis_ads
    path("ad_dis_list/",sm_views.ad_dis_list),
    path("view_addis_id/<id>",sm_views.view_addis_id),
    path("addistributor_ads/",sm_views.addistributor_ads),
    path("addis_ads_id/<id>",sm_views.addis_ads_id),
    path("adsdis_status_active/<id>",sm_views.adsdis_status_active),
    path("adsdis_status_reject/<id>",sm_views.adsdis_status_reject),


#/////////client add/////////
    path("add_client_data/<id>",sm_views.add_client_data),
    path("all_client_data/",sm_views.all_client_data),
    path("add_client_activities/<id>",sm_views.add_client_activities),
    path("all_activities/",sm_views.all_activities),
    path("view_client_id/<id>",sm_views.view_client_id),
    path("client_otp/<id>",sm_views.client_otp),
    path("sendmail/<id>",sm_views.sendmail),
    path("client_otp_active/<id>",sm_views.client_otp_active),
    path('active_satus/<id>',sm_views.active_satus),
   

    

#//////////Affiliate marketing///////////
    path('am_signup/',am_views.am_signup),
    path("am_otp/<id>",am_views.am_otp),
    path("am_signin/",am_views.am_signin),
    path("am_profile_picture/<id>",am_views.am_profile_picture),
    path("am_upload_account/<id>",am_views.am_upload_account),
    path("all_aff_data",am_views.all_aff_data),
    path("my_aff_data/<id>",am_views.my_aff_data),
    path("am_edit_account/<id>",am_views.am_edit_account),
    path("aff_email_update/<id>",am_views.aff_email_update),
    path("password_aff_reset/<id>",am_views.password_reset),
    path("pass_aff_update/<id>",am_views.pass_aff_update),
    path("af_my_data/<id>",am_views.af_my_data),
    path("add_user/<id>",am_views.add_user),
    path("am_my_users_data/<id>",am_views.my_users_data),
    path("single_users_data/<id>",am_views.single_users_data),
    path("all_aff_details",am_views.all_aff_details),
    path("aff_coin/<id>",am_views.aff_coin),
    path('aff_forget_password/',am_views.aff_forget_password),
    path('aff_forget_password_otp/<id>',am_views.aff_forget_password_otp),
    path('date_date/<id>',am_views.date_date),
    path('my_profile_finder_data/',am_views.my_profile_finder_data),

   

#//////////ad provider///////////
    path('ad_pro_signup/',ad_pro_views.ad_pro_signup),
    path('ad_pro_otp/<id>',ad_pro_views.ad_pro_otp),
    path('ad_pro_signin/',ad_pro_views.ad_pro_signin),
    path("ad_pro_profile_picture/<id>",ad_pro_views.ad_pro_profile_picture),
    path("ad_pro_upload_account/<id>",ad_pro_views.ad_pro_upload_account),
    path("ad_pro_my_data/<id>",ad_pro_views.ad_pro_my_data),
    path("all_ad_pro_data/",ad_pro_views.all_ad_pro_data),
    path("ad_pro_edit_account/<id>",ad_pro_views.ad_pro_edit_account),
    path('create_new_ads/<id>',ad_pro_views.create_new_ads),
    path('all_pro_ads_data/',ad_pro_views.all_pro_ads_data),
    path('ad_pro_ad_details/<id>',ad_pro_views.ad_pro_ad_details),
    path('ad_pro_edit_ads/<id>',ad_pro_views.ad_pro_edit_ads),
    path('ad_pro_email_update/<id>',ad_pro_views.ad_pro_email_update),
    path('ad_pro_password_update/<id>',ad_pro_views.ad_pro_password_update),
    path('ad_pro_password_reset/<id>',ad_pro_views.ad_pro_password_reset),
    path('ad_status_close/<id>',ad_pro_views.ad_status_close),
    path('ad_pro_deactive_update/<id>',ad_pro_views.ad_pro_deactive_update),
    path('status_deactive_to_active/<id>',ad_pro_views.status_deactive_to_active),
    path('ad_pro_add_user/<id>',ad_pro_views.ad_pro_add_user),
    path('ad_pro_my_users_data/<id>',ad_pro_views.ad_pro_my_users_data),
    path('ad_pro_single_users_data/<id>',ad_pro_views.ad_pro_single_users_data),
    path('ad_pro_forget_password/',ad_pro_views.ad_pro_forget_password),
    path('ad_pro_forget_password_otp/<id>',ad_pro_views.ad_pro_forget_password_otp),
    path('update_coin_value/<id>',ad_pro_views.update_coin_value),


#//////////ad distributor///////////
    path('ad_dis_signup/',ad_dis_views.ad_dis_signup),
    path('ad_dis_otp/<id>',ad_dis_views.ad_dis_otp),
    path('ad_dis_signin/',ad_dis_views.ad_dis_signin),
    path("ad_dis_profile_picture/<id>",ad_dis_views.ad_dis_profile_picture),
    path("ad_dis_upload_account/<id>",ad_dis_views.ad_dis_upload_account),
    path('all_ad_dis_data/',ad_dis_views.all_dis_data),
    path('ad_dis_my_data/<id>',ad_dis_views.dis_my_data),
    path('ad_dis_edit_account/<id>',ad_dis_views.ad_dis_edit_account),
    path('all_ads_data/',ad_dis_views.all_ads_data),
    path('create_ads/<id>',ad_dis_views.create_new_ads),
    path('ad_dis_ad_details/<id>',ad_dis_views.ad_dis_ad_details),
    path('ad_dis_edit_ads/<id>',ad_dis_views.ad_dis_edit_ads),
    path('ad_dis_email_update/<id>',ad_dis_views.ad_dis_email_update),
    path('ad_dis_password_update/<id>',ad_dis_views.ad_dis_password_update),
    path('ad_dis_password_reset/<id>',ad_dis_views.ad_dis_password_reset),
    path('ad_dis_status_close/<id>',ad_dis_views.ad_dis_status_close),
    path('ad_dis_deactive_update/<id>',ad_dis_views.ad_dis_deactive_update),
    path('ad_status_deactive_to_active/<id>',ad_dis_views.status_deactive_to_active),
    path("ad_dis_my_data/<id>",ad_dis_views.ad_dis_my_data),
    path('ad_dis_add_user/<id>',ad_dis_views.ad_dis_add_user),
    path('ad_dis_my_users_data/<id>',ad_dis_views.ad_dis_my_users_data),
    path('ad_dis_single_users_data/<id>',ad_dis_views.ad_dis_single_users_data),
    path('ad_dis_forget_password/',ad_dis_views.ad_dis_forget_password),
    path('ad_dis_forget_password_otp/<id>',ad_dis_views.ad_dis_forget_password_otp),
    path('update_coin_value/<id>',ad_dis_views.update_coin_value) ,
     



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
