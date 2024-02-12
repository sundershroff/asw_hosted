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
from apiapp import pi_views_api, views
from virtualExpert import hm_views_api, pm_views_api,am_views,ad_pro_views,ad_dis_views, sm_views_api


from django.contrib import admin
from django.urls import path
from profile_manager import pm_views
from sales_manager import sm_views
from hiring_manager import hm_views
from ad_provider import ad_provider_views
from ad_distributor import ad_distributor_views
from private_investigator import pi_views
from affiliate_marketing import af_views
from django.conf import settings
from django.conf.urls.static import static
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
    path('superadmin/pi_settings/<id>',super_views.pi_settingss),  
    path('superadmin/pi_performance_calculations/<id>',super_views.pi_performance_calculations),  
    path('superadmin/super_admin_hm_signup',super_views.super_admin_hm_signup),  






    


#///////////private investigator///////////////////
    path('pi_signup/',pi_views_api.signup),
    path("pi_otp/<id>",pi_views_api.otp),
    path('pi_signin/',pi_views_api.signin),
    path('pi_profilePicture/<id>',pi_views_api.profilePicture),
    path('pi_complete_account/<id>',pi_views_api.pi_complete_account),
    path('pi_edit_account/<id>',pi_views_api.pi_edit_account),
    path("all_private_investigator_data",pi_views_api.all_pi_data),
    path("pi_my_data/<id>",pi_views_api.pi_my_data),
    path("pi_my_clients/<id>",pi_views_api.my_clients),
    path("total_ratings/<id>",pi_views_api.total_ratings),
    # pass reset
    path("privateinvest_password_reset/<id>",pi_views_api.password_reset),
    path('pass_privateInvestigator_update/<id>',pi_views_api.pass_privateInvestigator_update),
    path('pi_email_update/<id>',pi_views_api.pi_email_update),
    # forget password
    path('pi_forget_password/',pi_views_api.pi_forget_password),
    path('pi_forget_password_otp/<id>',pi_views_api.pi_forget_password_otp),





#//////////profile manager///////////
    path('pm_myid/<id>',pm_views_api.pm_myid),
    path('pm_signup/',pm_views_api.pm_signup),
    path("pm_signin/",pm_views_api.pm_signin),
    path("pm_otp/<id>",pm_views_api.pm_otp),
    path("pm_profile_picture/<id>",pm_views_api.pm_profile_picture),
    path("pm_complete_account/<id>",pm_views_api.pm_complete_account),
    path("pm_edit_account/<id>",pm_views_api.pm_edit_account),
    path("all_pm_data/",pm_views_api.all_pm_data),
    path("pm_my_data/<id>",pm_views_api.pm_my_data),
    path("pm_my_clients/<id>",pm_views_api.my_clients),
    #status
    path("status/<id>",pm_views_api.pf_status),
    #users
    path("add_user/<id>",pm_views_api.add_user),
    path("pm_my_users_data/<id>",pm_views_api.my_users_data),
    path("single_users_data/<id>",pm_views_api.single_users_data),
    # email reset
    path('pm_email_update/<id>',pm_views_api.pm_email_update),
    # password reset
    path('pm_password_update/<id>',pm_views_api.pm_password_update),
    path('pm_password_reset/<id>',pm_views_api.pm_password_reset),
    # Forget password
    path('pm_forget_password/',pm_views_api.pm_forget_password),
    path('pm_forget_password_otp/<id>',pm_views_api.pm_forget_password_otp),
    
    

    


    



#//////////hiring manager///////////
    path('hm_signup/',hm_views_api.hm_signup),
    path("hm_otp/<id>",hm_views_api.hm_otp),
    path("hm_signin/",hm_views_api.hm_signin),
    path("hm_profile_picture/<id>",hm_views_api.hm_profile_picture),
    path("hm_upload_account/<id>",hm_views_api.hm_upload_account),
    path("hm_edit_account/<id>",hm_views_api.hm_edit_account),
    path("hm_my_data/<id>",hm_views_api.hm_my_data),
    path("all_hm_data/",hm_views_api.all_hm_data),
    path("profile_manager_upload_account/<id>",hm_views_api.profile_manager_upload_account),
    path("ad_provider_upload_account/<id>",hm_views_api.ad_provider_upload_account),
    path("ad_distributor_upload_account/<id>",hm_views_api.ad_distributor_upload_account),
    path("sales_upload_account/<id>",hm_views_api.sales_upload_account),
    path("hiring_upload_account/<id>",hm_views_api.hiring_upload_account),
    path("affiliate_upload_account/<id>",hm_views_api.affiliate_upload_account),
    path("private_investigator_upload_account/<id>",hm_views_api.private_investigator_upload_account),

    path("hm_add_user/<id>",hm_views_api.add_user),
    path("hm_my_users_data/<id>",hm_views_api.my_users_data),
    path("single_users_data/<id>",hm_views_api.single_users_data),

    path('hm_email_update/<id>',hm_views_api.hm_email_update),
    path('hm_password_reset/<id>',hm_views_api.hm_password_reset),
    path('hm_password_update/<id>',hm_views_api.hm_password_update),
    
    path('hm_forget_password/',hm_views_api.hm_forget_password),
    path('hm_forget_password_otp/<id>',hm_views_api.hm_forget_password_otp),
    


#//////////sales manager///////////
    path('sm_signup/',sm_views_api.sm_signup),
    path("sm_otp/<id>",sm_views_api.sm_otp),
    path("sm_signin/",sm_views_api.sm_signin),
    path("sm_profile_picture/<id>",sm_views_api.sm_profile_picture),
    path("sm_upload_account/<id>",sm_views_api.sm_upload_account),
    path("all_sm_data/",sm_views_api.all_sm_data),
    path("sm_my_data/<id>",sm_views_api.sm_my_data),
    path("sm_edit_data/<id>",sm_views_api.sm_edit_data),
    path("sm_email_update/<id>",sm_views_api.sm_email_update),
    path("password_reset/<id>",sm_views_api.password_reset),
    path("pass_sales_update/<id>",sm_views_api.pass_sales_update),
    path("sm_add_user/<id>",sm_views_api.add_user),
    path("sm_my_users_data/<id>",sm_views_api.my_users_data),
    path("single_users_data/<id>",sm_views_api.single_users_data),
    path('sales_forget_password/',sm_views_api.sales_forget_password),
    path('sales_forget_password_otp/<id>',sm_views_api.sales_forget_password_otp),
    
    # ad_pro_ads
    path("adprovider_ads/",sm_views_api.adprovider_ads),
    path("ad_pro_list/",sm_views_api.ad_pro_list),
    path("view_adpro_id/<id>",sm_views_api.view_adpro_id),
    path("addpro_ads_id/<id>",sm_views_api.addpro_ads_id),
    path("adspro_status_active/<id>",sm_views_api.adspro_status_active),
    path("adspro_status_reject/<id>",sm_views_api.adspro_status_reject),
    # ad_dis_ads
    path("ad_dis_list/",sm_views_api.ad_dis_list),
    path("view_addis_id/<id>",sm_views_api.view_addis_id),
    path("addistributor_ads/",sm_views_api.addistributor_ads),
    path("addis_ads_id/<id>",sm_views_api.addis_ads_id),
    path("adsdis_status_active/<id>",sm_views_api.adsdis_status_active),
    path("adsdis_status_reject/<id>",sm_views_api.adsdis_status_reject),


#/////////client add/////////
    path("add_client_data/<id>",sm_views_api.add_client_data),
    path("all_client_data/",sm_views_api.all_client_data),
    path("add_client_activities/<id>",sm_views_api.add_client_activities),
    path("all_activities/",sm_views_api.all_activities),
    path("view_client_id/<id>",sm_views_api.view_client_id),
    path("client_otp/<id>",sm_views_api.client_otp),
    path("sendmail/<id>",sm_views_api.sendmail),
    path("client_otp_active/<id>",sm_views_api.client_otp_active),
    path('active_satus/<id>',sm_views_api.active_satus),
   

    

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
    path("am_add_user/<id>",am_views.add_user),
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
#####################################------------------------------------------------###################     






##################-----------------------------------------------############################
    path('', pm_views.dashboard),
#///////profle manager//////
    path('profile_manager/signup/', pm_views.signup),
    path('profile_manager/signin/', pm_views.signin),
    path('profile_manager/otp/<id>', pm_views.otp),
    path('profile_manager/profile_picture/<id>', pm_views.profile_picture),
    path('profile_manager/upload_acc/<id>', pm_views.upload_acc),
    path('profile_manager/admin_dashboard/<id>', pm_views.admin_dashboard),
    path('profile_manager/profile_account/<id>', pm_views.profile_account),
    path('profile_manager/edit_acc/<id>', pm_views.edit_acc),
    path('profile_manager/acc_balance/<id>', pm_views.acc_balance),
    path('profile_manager/profile_finders/<id>', pm_views.profile_finders),
    path('profile_manager/view_details/<id>', pm_views.view_details),
    path('profile_manager/complaints/<id>', pm_views.complaints),
    path('profile_manager/users/<id>', pm_views.users),
    path('profile_manager/add_user/<id>', pm_views.add_user),
    path('profile_manager/user_edit/<id>', pm_views.user_edit),
    path('profile_manager/profile_finders_approved_list/<id>',pm_views.profile_finders_approved_list),
    path('profile_manager/settings/<id>', pm_views.settings),
    path('profile_manager/logout_view',pm_views.logout_view),
    path('pm_password_resett/<id>',pm_views.pm_password_reset),
    path('pm_forget_passwordd/',pm_views.pm_forget_password),
    path('pm_forgetpassword_otpp/<id>',pm_views.pm_forgetpassword_otp),
    path('pm_forgetpassword_resett/<id>',pm_views.pm_forgetpassword_reset),

#///////sales manager//////
    #///////sales manager//////
    path('sales_manager/signup/', sm_views.signup),
    path('sales_manager/signin/', sm_views.signin),
    path('sales_manager/otp/<id>', sm_views.otp),
    path('sales_manager/profile_picture/<id>', sm_views.profile_picture),
    path('sales_manager/sm_upload_profile/<id>', sm_views.upload_acc),
    path('sales_manager/sm_verification_fee/<id>', sm_views.verification_fee),
    path('sales_manager/sm_salesdashboard/<id>', sm_views.admin_dashboard),
    path('sales_manager/sm_sales_profile/<id>', sm_views.profile),
    path('sales_manager/sm_editprofile/<id>', sm_views.edit_profile),
    path('sales_manager/sm_accountbalance/<id>', sm_views.account_balance),
    path('sales_manager/sm_coindetails/<id>', sm_views.coin_details),
    path('sales_manager/sm_hand_list/<id>', sm_views.hand_list),
    path('sales_manager/sm_ads_list/<id>', sm_views.ads_list),
    path('sales_manager/sm_ad_details/<id>', sm_views.ad_details),
    path('sales_manager/sm_ad_dis_details/<id>',sm_views.ad_dis_details),
    path('sales_manager/sm_edit_adDetail/<id>', sm_views.edit_ad_details),
    path('sales_manager/sm_accountsetting/<id>', sm_views.setting),
    path('sales_manager/sm_users/<id>', sm_views.users),
    path('sales_manager/sm_addusers/<id>', sm_views.add_users),
    path('sales_manager/sm_user_edit/<id>', sm_views.sm_user_edit),
    path('sales_manager/sm_client_details/<id>',sm_views.sm_client_details),
    path('sales_manager/otp_client/<id>',sm_views.otp_client),
    path('password_resett/<id>',sm_views.password_reset),
    # path('sales_manager/add_client/<id>',sm_views.add_client),
    path("sales_manager/ad_pro_ads/<id>",sm_views.ad_pro_ads),
    # path("sales_manager/ad_proads_details/<id>",sm_views.ad_proads_details),
    path('sales_forget_passwordd/',sm_views.sales_forget_password),
    path('sales_forgetpassword_otpp/<id>',sm_views.sales_forgetpassword_otp),
    path('sales_forgetpassword_resett/<id>',sm_views.sales_forgetpassword_reset),
    path('sales_manager/sm_edit_adproDetail/<id>',sm_views.edit_adpro_details),
    path("sales_manager/signout",sm_views.signout),




#///////hiring manager//////
    path('hiring_manager/signup/', hm_views.signup),
    path('hiring_manager/signin/', hm_views.signin),
    path('hiring_manager/otp/<id>', hm_views.otp),
    path('hiring_manager/profile_picture/<id>', hm_views.profile_picture),
    path('hiring_manager/hm_upload_acc/<id>', hm_views.upload_acc),
    path('hiring_manager/hm_admin_dashboard/<id>', hm_views.admin_dashboard),
    path('hiring_manager/hm_profile/<id>', hm_views.profile),
    path('hiring_manager/hm_edit_acc/<id>', hm_views.edit_acc),
    path('hiring_manager/hm_local_admin/<id>', hm_views.local_admin),
    path('hiring_manager/hm_local_admin_upload/<id>', hm_views.local_admin_upload),
    path('hiring_manager/hm_ad_provider/<id>', hm_views.ad_provider),
    path('hiring_manager/hm_adprovider_upload/<id>', hm_views.ad_provider_doc),
    path('hiring_manager/hm_ad_distributor/<id>', hm_views.ad_distributor),
    path('hiring_manager/hm_ad_distributor_upload/<id>', hm_views.ad_distributor_doc),
    path('hiring_manager/hm_sales_person/<id>', hm_views.sales),
    path('hiring_manager/hm_sales_person_doc/<id>', hm_views.sales_doc),
    path('hiring_manager/hm_affiliate_marketing/<id>', hm_views.affiliate_marketing),
    path('hiring_manager/hm_affiliate_marketing_upload/<id>', hm_views.affiliate_marketing_doc),
    path('hiring_manager/hm_private_investigator/<id>', hm_views.private_investigator),
    path('hiring_manager/hm_private_investigator_upload/<id>', hm_views.private_investigator_doc),
    path('hiring_manager/hm_hiring_manager/<id>', hm_views.hiring_manager),
    path('hiring_manager/hm_hiring_manager_doc/<id>', hm_views.hiring_manager_doc),
    path('hiring_manager/hm_settings/<id>', hm_views.setting),
    path('hiring_manager/hm_users/<id>', hm_views.users),
    path('hiring_manager/hm_addusers/<id>', hm_views.add_users),
    path('hiring_manager/hm_user_edit/<id>', hm_views.hm_user_edit),
    path('hm_password_resett/<id>',hm_views.hm_password_reset),
    path('hm_forget_passwordd/',hm_views.hm_forget_password),
    path('hm_forgetpassword_otpp/<id>',hm_views.hm_forgetpassword_otp),
    path('hm_forgetpassword_resett/<id>',hm_views.hm_forgetpassword_reset),
    path('hm_logout',hm_views.logout_view),




#///////ad_provider manager//////
    path('ad_provider/signup/', ad_provider_views.signup),
    path('ad_provider/signin/', ad_provider_views.signin),
    path('ad_provider/otp/<id>', ad_provider_views.otp),
    path('ad_provider/profile_picture/<id>', ad_provider_views.profile_picture),
    path('ad_provider/upload_acc/<id>', ad_provider_views.upload_acc),
    path('ad_provider/ad_provider_admin_dashboard/<id>', ad_provider_views.admin_dashboard),
    path('ad_provider/ad_pro_account/<id>', ad_provider_views.account), 
    path('ad_provider/ad_pro_editAccount/<id>', ad_provider_views.edit_account),
    path('ad_provider/ad_pro_acc_balance/<id>', ad_provider_views.acc_balance),
    path('ad_provider/ad_pro_adFunds/<id>', ad_provider_views.add_funds),
    path('ad_provider/ad_pro_list/<id>', ad_provider_views.ads_list_all),
    path('ad_provider/ad_pro_active/<id>', ad_provider_views.ads_active),
    path('ad_provider/ad_pro_pending/<id>', ad_provider_views.ads_pending),
    path('ad_provider/ad_pro_deactive/<id>', ad_provider_views.ads_deactive),
    path('ad_provider/ad_pro_closed/<id>', ad_provider_views.ads_closed),
    path('ad_provider/ad_pro_createAd/<id>', ad_provider_views.ad_pro_createAd),
    path('ad_provider/ad_pro_payment/<id>', ad_provider_views.ad_pro_payment),
    path('ad_provider/ad_pro_editAd/<id>', ad_provider_views.ad_pro_editAd),
    path('ad_provider/ad_pro_adDetails/<id>', ad_provider_views.ad_pro_adDetails),
    path('ad_provider/ad_pro_users/<id>', ad_provider_views.ad_pro_users),
    path('ad_provider/ad_pro_addusers/<id>', ad_provider_views.ad_pro_addusers),
    path('ad_provider/ad_pro_user_edit/<id>', ad_provider_views.ad_pro_user_edit),
    path('ad_provider/ad_pro_settings/<id>', ad_provider_views.ad_pro_settings),
    path('ad_pro_password_resett/<id>',ad_provider_views.ad_pro_password_reset),
    path('ad_provider/ad_pro_coins/<id>',ad_provider_views.ad_pro_coins),
    path('ad_pro_forget_passwordd/',ad_provider_views.ad_pro_forget_password),
    path('ad_pro_forgetpassword_otpp/<id>',ad_provider_views.ad_pro_forgetpassword_otp),
    path('ad_pro_forgetpassword_resett/<id>',ad_provider_views.ad_pro_forgetpassword_reset),
    path('ad_provider/logout_view',ad_provider_views.logout_view),
 




#///////ad_distributor manager//////
    path('ad_distributor/signup/', ad_distributor_views.signup),
    path('ad_distributor/signin/', ad_distributor_views.signin),
    path('ad_distributor/otp/<id>', ad_distributor_views.otp),
    path('ad_distributor/profile_picture/<id>', ad_distributor_views.profile_picture),
    path('ad_distributor/upload_acc/<id>', ad_distributor_views.upload_acc),
    path('ad_distributor/ad_distributor_admin_dashboard/<id>', ad_distributor_views.admin_dashboard),
    path('ad_distributor/ad_dis_account/<id>', ad_distributor_views.account),
    path('ad_distributor/ad_dis_editAccount/<id>', ad_distributor_views.edit_account),
    path('ad_distributor/ad_dis_acc_balance/<id>', ad_distributor_views.acc_balance),
    path('ad_distributor/ad_dis_adFunds/<id>', ad_distributor_views.add_funds),
    path('ad_distributor/ad_dis_list/<id>', ad_distributor_views.ads_list_all),
    path('ad_distributor/ad_dis_active/<id>', ad_distributor_views.ads_active),
    path('ad_distributor/ad_dis_pending/<id>', ad_distributor_views.ads_pending),
    path('ad_distributor/ad_dis_deactive/<id>', ad_distributor_views.ads_deactive),
    path('ad_distributor/ad_dis_closed/<id>', ad_distributor_views.ads_closed),
    path('ad_distributor/ad_dis_createAd/<id>', ad_distributor_views.ad_dis_createAd),
    path('ad_distributor/ad_dis_payment/<id>', ad_distributor_views.ad_dis_payment),
    path('ad_distributor/ad_dis_editAd/<id>', ad_distributor_views.ad_dis_editAd),
    path('ad_distributor/ad_dis_adDetails/<id>', ad_distributor_views.ad_dis_adDetails),
    path('ad_distributor/ad_dis_users/<id>', ad_distributor_views.ad_dis_users),
    path('ad_distributor/ad_dis_addusers/<id>', ad_distributor_views.ad_dis_addusers),
    path('ad_distributor/ad_dis_user_edit/<id>', ad_distributor_views.ad_dis_user_edit),
    path('ad_distributor/ad_dis_settings/<id>', ad_distributor_views.ad_dis_settings),
    path('ad_dis_password_resett/<id>',ad_distributor_views.ad_dis_password_reset),
    path('ad_distributor/ad_dis_coins/<id>', ad_distributor_views.ad_dis_coins),
    path('ad_dis_forget_passwordd/',ad_distributor_views.ad_dis_forget_password),
    path('ad_dis_forgetpassword_otpp/<id>',ad_distributor_views.ad_dis_forgetpassword_otp),
    path('ad_dis_forgetpassword_resett/<id>',ad_distributor_views.ad_dis_forgetpassword_reset),
    path('ad_distributor/logout_view',ad_distributor_views.logout_view),

    


#///////affiliate_marketing manager//////
    path('affiliate_marketing/signup/', af_views.signup),
    path('affiliate_marketing/signin/', af_views.signin),
    path('affiliate_marketing/otp/<id>', af_views.otp),
    path('affiliate_marketing/profile_picture/<id>', af_views.profile_picture),
    path('affiliate_marketing/af_uploadprofile/<id>', af_views.upload_acc),
    path('affiliate_marketing/af_profile/<id>', af_views.profile),
    path('affiliate_marketing/af_editprofile/<id>', af_views.edit_profile),
    path('affiliate_marketing/af_commisions/<id>', af_views.commisions),
    path('affiliate_marketing/af_setting/<id>', af_views.setting),
    path('affiliate_marketing/af_marketingdashboard/<id>',af_views.admin_dashboard),
    path('password_aff_resett/<id>',af_views.password_reset),
    path('affiliate_marketing/am_users/<id>', af_views.users),
    path('affiliate_marketing/am_addusers/<id>', af_views.add_users),
    path('affiliate_marketing/am_user_edit/<id>', af_views.am_user_edit),
    path('aff_forget_passwordd/',af_views.aff_forget_password),
    path('aff_forgetpassword_otpp/<id>',af_views.aff_forgetpassword_otp),
    path('aff_forgetpassword_resett/<id>',af_views.aff_forgetpassword_reset),
    path('affiliate_marketing/signout',af_views.signout),

#///////////////////private investagator////////////////////
    path('pi_signin', pi_views.signin),
    path('pi_signup', pi_views.signup),
    path('pi_otpcheck/<id>', pi_views.opt_check),
    path('pi_profilepicture/<id>', pi_views.profile_picture),
    path('pi_complete_profile/<id>', pi_views.complete_profile),
    path('pi_admin_dashboard/<id>', pi_views.admin_dashboard),
    path('pi_profile/<id>', pi_views.profile),
    path('edit_profile/<id>', pi_views.edit_profile),
    path('pi_payment_screen/<id>', pi_views.payment),
    path('pi_client_list/<id>', pi_views.client_list),
    path('pi_client_details/<id>', pi_views.client_details),
    path('pi_subscription/<id>', pi_views.subscription),
    path('pi_payment_table/<id>', pi_views.payment_table),
    path('pi_add_client/<id>', pi_views.add_client),
    path('pi_client_feedback/<id>', pi_views.client_feedback),
    path('pi_setting/<id>', pi_views.setting),
    # pass reset
    path('privateinvest_password_resett/<id>',pi_views.password_reset),
    # forget password
    path('pi_forget_passwordd/',pi_views.pi_forget_password),
    path('pi_forgetpassword_otpp/<id>/',pi_views.pi_forgetpassword_otp),
    path('pi_forgetpassword_resett/<id>/',pi_views.pi_forgetpassword_reset),
    path('pi_logout',pi_views.pi_logout),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
