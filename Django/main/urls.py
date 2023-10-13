from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('delete/<str:model>/<int:instance_id>/<int:next_id>', views.delete_view, name='delete'), # Editor Only
    path('delete/<str:model>/<int:instance_id>', views.delete_view, name='delete_noreturn'), # Editor Only
    path('robots', views.robot_index_view, name='robotIndex'), # Everyone
    path('robot/<str:slug>', views.robot_detail_view, name='robotDetail'), # Everyone
    path('robots/<int:robot_id>/transfer', views.robot_transfer_view, name='transferRobot_form'), # Should this even be here - Editor Only
    path('robots/<int:robot_id>/transfer/<int:team_id>', views.robot_transfer_view, name='transferRobot'), # Should this even be here - Editor Only
    path('robots/<int:robot_id>/edit', views.robot_edit_view, name='editRobot'), #Editor Only
    path('robots/new', views.new_robot_view, name='newRobot'), # Editor Only
    path('leaderboard', views.leaderboard, name="leaderboard"), # Everyone
    path('events', views.event_index_view, name='eventIndex'), # Everyone
    path('event/<slug:slug>', views.event_detail_view, name='eventDetail'), # Everyone
    path('events/new/<int:franchise_id>', views.new_event_view, name='newEvent'), # Editor Only
    path('events/<int:event_id>/edit', views.modify_event_view, name='editEvent'), # Editor Only
    path('contest/<int:contest_id>', views.contest_detail_view, name='contestDetail'), # Everyone
    path('contests/new/<int:event_id>', views.new_contest_view, name='newContest'), # Editor Only
    path('contests/<int:contest_id>/edit', views.edit_contest_view, name='editContest'), # Editor Only
    path('teams', views.team_index_view, name='teamIndex'), # Everyone
    path('teams/<int:team_id>/edit', views.team_modify_view, name='editTeam'),  # Editor Only
    path('teams/new', views.team_modify_view, name='newTeam'), # Editor Only
    path('team/<slug:slug>', views.team_detail_view, name='teamDetail'), #Everyone
    path('franchises', views.franchise_index_view, name='franchiseIndex'), #Everyone
    path('franchises/<int:franchise_id>/edit', views.franchise_modify_view, name='editFranchise'), # Editor Only
    path('franchises/new', views.franchise_modify_view, name='newFranchise'),# Editor Only
    path('franchise/<slug:slug>', views.franchise_detail_view, name='franchiseDetail'),#Everyone
    path('fights/new/<int:contest_id>', views.new_fight_view, name='newFight'), #Editor only
    path('fight/<int:fight_id>', views.fight_detail_view, name='fightDetail'),
    path('fight/<int:fight_id>/edit', views.fight_editj_view, name='editJustFight'),
    path('fights/<int:fight_id>/addRobot', views.modify_fight_version_view, name='newFightVersion'),
    path('fights/<int:fight_id>/editRobot/<int:vf_id>', views.modify_fight_version_view, name='editFightVersion'),
    path('version/<int:version_id>', views.version_detail_view, name='versionDetail'),
    path('versions/<int:version_id>/edit', views.version_edit_view, name='editVersion'),
    path('versions/new/<int:robot_id>', views.new_version_view, name='newVersion'),
    path('event/<slug:event_slug>/awards', views.award_index_view, name='awardIndex'),
    path('awards/new/<int:event_id>', views.new_award_view, name='newAward'),
    path('weight_class/new/<int:return_id>', views.new_weight_class_view, name='newWeightClass'),
    path('awards/<int:award_id>/edit', views.award_edit_view, name='editAward'),
    path('account_public_details/<int:person_id>/edit', views.person_edit_view, name='editPerson'),
    #path('accounts/register', views.register, name='register'),
    #path('accounts/profile/', views.profile_view, name='profile'),
    path('<str:obj_type>/add_member/<int:obj_id>', views.add_member_view, name="addMember"),
    path('hall-of-fame', views.hall_of_fame_view, name="hallOfFame"),
    path('search', views.search_view, name="search"),
    path('message', views.message_view, name='message'),
    path('credits', views.credits_view, name='credits'),

    path('editor/home', views.edt_home_view, name='edtHome'),
    path('editor/newEvent', views.edt_new_event_view, name='edtNewEvent'),
    path('editor/event/<int:event_id>', views.edt_event_view, name='edtEvent'),
    path('editor/contest/<int:contest_id>', views.edt_contest_view, name='edtContest'),
    path('editor/selectFranchise', views.edt_fran_view, name='edtSelectFran'),
    path('editor/fight/<int:fight_id>', views.edt_fight_view, name='edtFightOverview'),
    path('editor/selectRobot', views.edt_select_robot_view, name='edtSelectRobot'), # Modifyfightversion
    path('editor/fight/selectVersion/<int:robot_id>', views.edt_select_version_view, name='edtSelectVersion'),
    path('editor/fight/<int:fight_id>/signupVersion/<int:version_id>', views.edt_signup_version_view, name='edtSignupVersion'),
    path('editor/fight/<int:fight_id>/selectTeam', views.edt_select_team_view, name='edtSelectTeam'),
    path('editor/team/<int:team_id>', views.edt_team_view, name='edtTeam'),
    path('editor/link/<str:obj_type>/<int:obj_id>', views.edt_team_view, name='edtLink'),
    #path('editor/recalculate', views.recalc_all, name='recalculateAll'),
    #path('test/tourny', views.tournament_tree, name='tournament_test'),
    #path('import', views.importView, name='import'),
    #path('test/graph', views.graph_test, name='graph_test'),
    #path('test/graph_data', views.graph_data, name='graph_test'),
]
