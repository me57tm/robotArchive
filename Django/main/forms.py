import datetime
import urllib
import time
from io import BytesIO
from PIL import Image
from django.core.files import File

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Max

from .models import *


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewRobotForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    vname = forms.CharField(max_length=255, required=False, label="Name of first version if different from main name")
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    img = forms.ImageField(required=False)
    weapon_type = forms.CharField(max_length=20, required=True)
    weight_class = forms.ModelChoiceField(queryset=Weight_Class.objects.all().order_by("-recommended", "weight_grams"),
                                          required=True)
    opt_out = forms.BooleanField(required=False)

    def save(self, team, owner):
        r = Robot()
        v = Version()
        r.name = self.cleaned_data['name']
        v.robot_name = self.cleaned_data['vname']
        r.country = self.cleaned_data['country']
        v.country = self.cleaned_data['country']
        r.description = self.cleaned_data['description']
        r.opt_out = self.cleaned_data['opt_out']
        v.robot = r
        v.image = self.cleaned_data['img']
        v.weapon_type = self.cleaned_data['weapon_type']
        v.weight_class = self.cleaned_data['weight_class']
        v.owner = owner
        if team != 0:
            v.team = team
        r.save()
        v.save()
        return r, v


class NewVersionForm(forms.Form):
    robot_name = forms.CharField(max_length=255, required=False)
    version_name = forms.CharField(max_length=255, required=False)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    img = forms.ImageField(required=False)
    weapon_type = forms.CharField(max_length=20, required=True)
    weight_class = forms.ModelChoiceField(queryset=Weight_Class.objects.all().order_by("-recommended", "weight_grams"),
                                          required=True)
    team = forms.ModelChoiceField(queryset=None, required=False)

    def save(self, robot, owner):
        v = Version()
        v.robot = robot
        if self.cleaned_data['country'] and self.cleaned_data['country'] != "XX":
            v.country = self.cleaned_data['country']
        else:
            v.country = robot.country
        v.robot_name = self.cleaned_data['robot_name']
        v.name = self.cleaned_data['version_name']
        v.description = self.cleaned_data['description']
        v.image = self.cleaned_data['img']
        v.weapon_type = self.cleaned_data['weapon_type']
        v.weight_class = self.cleaned_data['weight_class']
        v.team = self.cleaned_data['team']
        v.owner = owner
        v.save()
        return v


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['name', 'description', "opt_out"]


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ["robot_name", "name", "country", "description", "image", "weapon_type", "weight_class"]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'logo', 'country']


class FranchiseForm(forms.ModelForm):  # TODO: Add Web Links
    class Meta:
        model = Franchise
        fields = ['name', 'description', 'logo']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'logo', 'country', 'start_date', 'end_date', 'franchise']


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ["name", "fight_type", "weight_class"]


class FightForm(forms.ModelForm):
    class Meta:
        model = Fight
        fields = ["name", "fight_type", "method", "internal_media", "external_media"]


class RobotFightForm(forms.ModelForm):
    class Meta:
        model = Fight_Version
        fields = ["version", "won", "tag_team"]


class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['name', 'award_type', 'contest', 'version']


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'public']


class WeightClassForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    weight_grams = forms.IntegerField(initial=0, min_value=0, required=True)

    # Requires Javascript
    # weight_kg = forms.IntegerField(initial=0, min_value=0)
    # weight_lbs = forms.IntegerField(initial=0, min_value=0)

    def save(self):
        wc = Weight_Class()
        wc.name = self.cleaned_data['name']
        wc.weight_grams = self.cleaned_data['weight_grams']
        wc.save()


class TransferRobotForm(forms.Form):
    team_name = forms.CharField(max_length=255, required=True)
    team_id = forms.IntegerField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        team_name = cleaned_data.get('team_name')
        team_id = cleaned_data.get('team_id')
        if team_name and team_id:
            try:
                Team.objects.get(name=team_name, pk=team_id)
            except ObjectDoesNotExist:
                raise ValidationError(
                    "A team with these details could not be found."
                )

    def save(self):
        team_name = self.cleaned_data.get('team_name')
        team_id = self.cleaned_data.get('team_id')
        new_team = Team.objects.get(name=team_name, pk=team_id)
        return new_team


class NewEventFormEDT(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    logo_img = forms.ImageField(required=False)
    logo_txt = forms.URLField(required=False)
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=False)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=True)

    def save(self, franchise):
        e = Event()
        e.name = self.cleaned_data['name']
        e.description = self.cleaned_data['description']
        e.start_date = self.cleaned_data['start_date']
        if not self.cleaned_data['end_date']:
            e.end_date = self.cleaned_data['start_date']
        else:
            e.end_date = self.cleaned_data['end_date']
        e.country = self.cleaned_data['country']
        e.franchise = franchise

        if not self.cleaned_data['logo_img'] and not self.cleaned_data['logo_txt']:
            pass
        elif not self.cleaned_data['logo_img']:
            save_img(self.cleaned_data['logo_txt'], e.logo, e.name)
        else:
            e.logo = self.cleaned_data['logo_img']

        e.save()
        return e


def save_img(img_link, var, file_name):
    az = re.compile("[^a-zA-Z0-9]")
    l = 0
    while True:
        if l > 10:
            break
        try:
            urllib.request.urlretrieve(img_link, "downloadImage")
            break
        except:
            print("failed to save image:", img_link, "attempt:", l + 1)
            time.sleep(2)
            l += 1
    if l > 10:
        print("IMAGE FAILED TO SAVE: " + file_name)
    img = Image.open("downloadImage")
    rawData = BytesIO()
    img.save(rawData, img.format)
    fname = re.sub(az, "", file_name)
    if len(fname) > 25:
        fname = fname[:25]
    var.save(fname + "." + img.format.lower(), File(rawData))
