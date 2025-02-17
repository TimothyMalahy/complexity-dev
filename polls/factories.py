import factory
from .models import Topic
from django.utils import timezone
import random
from .models import Vote, Subject
from user_app.models import CustomUser


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    topic_text = factory.LazyAttribute(
        lambda _: random.choice(
            [
                "C ",
                "Java ",
                "Python ",
                "C++ ",
                "C# ",
                "JavaScript ",
                "PHP ",
                "R ",
                "SQL",
                "Go",
                "Swift",
                "Perl",
                "Assembly language",
                "Visual Basic",
                "Ruby",
                "MATLAB",
                "Objective-C",
                "Rust",
                "Delphi/Object Pascal",
                "Classic Visual Basic",
                "SAS",
                "Scratch",
                "D",
                "Dart",
                "PL/SQL",
                "Logo",
                "COBOL",
                "Kotlin",
                "Julia",
                "ABAP",
                "Scala",
                "Transact-SQL",
                "Scheme",
                "Prolog",
                "Ada",
                "Lisp",
                "Apex",
                "Lua",
                "Fortran",
                "Haskell",
                "Hack",
                "VBScript",
                "TypeScript",
                "AWK",
                "ActionScript",
                "Tcl",
                "Smalltalk",
                "(Visual) FoxPro",
                "Solidity",
                "PowerShell",
                "ABC",
                "Algol",
                "APL",
                "Bash",
                "Carbon",
                "CFML",
                "CHILL",
                "CLIPS",
                "Clojure",
                "CLU",
                "Crystal",
                "Curl",
                "DiBOL",
                "Eiffel",
                "Elixir",
                "Elm",
                "Erlang",
                "F#",
                "Forth",
                "GAMS",
                "Groovy",
                "Icon",
                "Inform",
                "Io",
                "J",
                "JScript",
                "LabVIEW",
                "Ladder Logic",
                "ML",
                "Modula-2",
                "Mojo",
                "MQL5",
                "NATURAL",
                "Nim",
                "OCaml",
                "Occam",
                "OpenCL",
                "PL/I",
                "PureScript",
                "Q",
                "Ring",
                "RPG",
                "S",
                "SPARK",
                "Stata",
                "SystemVerilog",
                "VHDL",
                "Wolfram",
                "X++",
                "Zig",
            ]
        )
    )
    pub_date = factory.LazyFunction(timezone.now)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    user = factory.SubFactory(UserFactory)
    topic = factory.LazyAttribute(lambda _: Topic.objects.get(topic_text="CSS"))
    submitted = factory.LazyAttribute(lambda _: random.choice([True, False]))
    date_voted = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def rankings(self, create, extracted, **kwargs):
        if not create:
            return

        subjects = list(Subject.objects.filter(topic=self.topic))
        random.shuffle(subjects)
        self.rankings = {i + 1: subject.id for i, subject in enumerate(subjects)}

    @factory.post_generation
    def add_date_voteds(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for date in extracted:
                self.date_voteds.add(date)
        else:
            for _ in range(random.randint(1, 5)):
                self.date_voteds.add(
                    timezone.now() - timezone.timedelta(days=random.randint(1, 365))
                )
