from django.db import models
from django.conf import settings
import pycountry

FULL_COMBAT = 'FC'
SPORTSMAN = 'SP'
PLASTIC = 'PL'
NON_COMBAT = 'NC'
FIGHT_TYPE_CHOICES = [
    (FULL_COMBAT, "Full Combat"),
    (SPORTSMAN, "Sportsman"),
    (PLASTIC, "Restricted Material"),
    (NON_COMBAT, "Non-Combat")
    ]

COUNTRY_CHOICES = []
for country in pycountry.countries:
    COUNTRY_CHOICES.append((country.alpha_2,country.name))
COUNTRY_CHOICES.extend([
    ('XE',"England"),
    ('XS',"Scotland"),
    ('XW',"Wales"),
    ('XI',"Northern Ireland")
    ])

class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,blank=True,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length = 255)
    email = models.EmailField()
    def __str__(self):
    	return self.name

class Team(models.Model):
    name = models.CharField(max_length = 255)
    logo = models.ImageField(upload_to='team_logos/%Y/',blank=True)
    website = models.URLField(blank=True)
    country = models.CharField(max_length = 2,choices = COUNTRY_CHOICES)
    members = models.ManyToManyField(Person,through="Person_Team")
    def __str__(self):
    	return self.name
    
class Weight_Class(models.Model):
    name = models.CharField(max_length = 30)
    weight_grams = models.IntegerField()
    def __str__(self):
    	return self.name

class Robot(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(blank=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ranking = models.FloatField()
    opt_out = models.BooleanField(default=False) # for opting out of rankings
    def __str__(self):
    	return self.name

class Version(models.Model):
    robot_name = models.CharField(max_length = 255)
    version_name = models.CharField(max_length = 255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='robot_images/%Y/',blank=True)
    weapon_type = models.CharField(max_length = 20)
    robot = models.ForeignKey(Robot, on_delete = models.CASCADE)
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    weight_class = models.ForeignKey(Weight_Class, on_delete = models.CASCADE)
    def __str__(self):
    	return self.robot_name + " " + self.version_name

class Franchise(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='franchise_logos/%Y/',blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(Person,through="Person_Franchise")
    def __str__(self):
    	return self.name

class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='event_logos/%Y/',blank=True)
    ruleset = models.FileField(upload_to='event_rulesets')
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    registration_close = models.DateTimeField()
    country = models.CharField(max_length = 2,choices = COUNTRY_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    franchise = models.ForeignKey(Franchise,on_delete = models.CASCADE)
    def __str__(self):
        return self.name

class Contest(models.Model):
	name = models.CharField(max_length=50,blank=True)
	fight_type = models.CharField(max_length = 2, choices = FIGHT_TYPE_CHOICES)
	auto_awards = models.BooleanField()
	event = models.ForeignKey(Event,on_delete = models.CASCADE)
	weight_class = models.ForeignKey(Weight_Class,on_delete = models.CASCADE)
	def __str__(self):
		if self.name != None and self.name != "":
			return self.name
		else:
			return self.weight_class.name

class Registration(models.Model):
    signup_time = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    reserve = models.BooleanField(default=False)
    version = models.ForeignKey(Version,on_delete = models.CASCADE)
    signee = models.ForeignKey(Person,on_delete = models.CASCADE)
    contest = models.ForeignKey(Contest,on_delete = models.CASCADE)

class Fight(models.Model):
    METHOD_CHOICES = [
        ("KO","Knockout"),
        ("JD","Judge's Decision"),
        ("TO","Tap Out"),
        ("OA","Out of the Arena"),
        ("PT","Pit"),
        ("DR","Draw"),
        ("WU","Winner Unknown"),
        ("NW","No Winner Declared"),
        ("NM","No Method Declared"),
        ]
    method = models.CharField(max_length = 2, choices = METHOD_CHOICES,default="NM")
    name = models.CharField(max_length=100)
    fight_type = models.CharField(max_length = 2, choices = FIGHT_TYPE_CHOICES)
    media_internal = models.FileField(upload_to='fight_media/%Y/',blank=True)
    media_external = models.URLField(blank=True);
    event = models.ForeignKey(Event,on_delete = models.CASCADE)
    contest = models.ForeignKey(Contest,on_delete = models.CASCADE,blank=True)
    competitors = models.ManyToManyField(Version,through="Fight_Version")
    def __str__(self):
    	return self.name

class Award(models.Model):
    name = models.CharField(max_length = 255)
    award_type = models.PositiveSmallIntegerField()#0 other, 1 first place, 2 second place, 3 thrid place
    contest = models.ForeignKey(Contest,on_delete = models.CASCADE)
    version = models.ForeignKey(Version,on_delete = models.CASCADE)
    def __str__(self):
    	return self.name

class Person_Team(models.Model):
    person = models.ForeignKey(Person,on_delete = models.CASCADE)
    team = models.ForeignKey(Team,on_delete = models.CASCADE)

class Person_Franchise(models.Model):
    person = models.ForeignKey(Person,on_delete = models.CASCADE)
    franchise = models.ForeignKey(Franchise,on_delete = models.CASCADE)

class Fight_Version(models.Model):
    won = models.BooleanField()
    tag_team = models.PositiveSmallIntegerField() # matching number, matching side on a tag team match, 0 for free for all fights
    fight = models.ForeignKey(Fight,on_delete = models.CASCADE)
    version = models.ForeignKey(Version,on_delete = models.CASCADE)
