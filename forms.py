# Christiano Blairoy Fernandes
# 23f2004927
# 12 April 2026
# forms.py


from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    FloatField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import (
    URL,
    DataRequired,
    EqualTo,
    Length,
    NumberRange,
    Optional,
    Regexp,
    ValidationError,
)


class StudentRegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=40)]
    )

    email = StringField("Email", validators=[
        DataRequired(),Regexp(r'^[^@]+@[^@]+\.[^@]+$', message="Enter a valid email address.")
])

    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    full_name = StringField(
        "Full Name", validators=[DataRequired(), Length(min=2, max=100)]
    )

    department = StringField(
        "Department", validators=[DataRequired(), Length(min=2, max=100)]
    )

    graduation_year = IntegerField(
        "Graduation Year",
        validators=[
            DataRequired(),
            NumberRange(min=datetime.now().year - 10, max=datetime.now().year + 4),
        ],
    )

    cgpa = FloatField("CGPA", validators=[Optional(), NumberRange(min=0.0, max=10.0)])


class CompanyRegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=40)]
    )

    email = StringField("Email", validators=[
        DataRequired(),
        Regexp(r'^[^@]+@[^@]+\.[^@]+$', message="Enter a valid email address.")
    ])

    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    company_name = StringField(
        "Company Name", validators=[DataRequired(), Length(min=2, max=120)]
    )

    hr_contact = StringField("HR Contact", validators=[Optional(), Length(max=100)])

    website = StringField(
        "Website", validators=[Optional(), URL(message="Enter a valid URL.")]
    )

    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=1000)]
    )


class StudentProfileForm(FlaskForm):
    full_name = StringField(
        "Full Name", validators=[DataRequired(), Length(min=2, max=100)]
    )

    department = StringField(
        "Department", validators=[DataRequired(), Length(min=2, max=100)]
    )

    graduation_year = IntegerField(
        "Graduation Year",
        validators=[
            DataRequired(),
            NumberRange(min=datetime.now().year - 10, max=datetime.now().year + 4),
        ],
    )

    cgpa = FloatField("CGPA", validators=[Optional(), NumberRange(min=0.0, max=10.0)])

    gender = SelectField(
        "Gender",
        choices=[
            ("", "Prefer not to say"),
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other"),
        ],
        validators=[Optional()],
    )

    skills = TextAreaField("Skills", validators=[Optional(), Length(max=1000)])

    linkedin = StringField(
        "LinkedIn", validators=[Optional(), URL(message="Enter a valid LinkedIn URL.")]
    )

    github = StringField(
        "GitHub", validators=[Optional(), URL(message="Enter a valid GitHub URL.")]
    )


class CompanyProfileForm(FlaskForm):
    company_name = StringField(
        "Company Name", validators=[DataRequired(), Length(min=2, max=120)]
    )

    industry = StringField("Industry", validators=[Optional(), Length(max=100)])

    hr_contact = StringField("HR Contact", validators=[Optional(), Length(max=100)])

    website = StringField(
        "Website", validators=[Optional(), URL(message="Enter a valid URL.")]
    )

    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=1000)]
    )   


class DriveForm(FlaskForm):
    drive_name = StringField(
        "Drive Name", validators=[DataRequired(), Length(min=2, max=120)]
    )

    job_title = StringField(
        "Job Title", validators=[DataRequired(), Length(min=2, max=120)]
    )

    job_type = SelectField(
        "Job Type",
        choices=[
            ("Full-Time", "Full-Time"),
            ("Internship", "Internship"),
            ("Contract", "Contract"),
        ],
        validators=[DataRequired()],
    )

    location = StringField("Location",
                    default="Remote",
                    validators=[DataRequired(), Length(max=120)])

    compensation = StringField(
        "Compensation (CTC)",
        default="Performance Based",
        validators=[Optional(), Length(max=80)]
    )

    application_deadline = DateField(
        "Application Deadline", validators=[DataRequired()]
    )

    eligibility_criteria = TextAreaField(
        "Eligibility Criteria", validators=[Optional(), Length(max=500)]
    )

    job_description = TextAreaField(
        "Job Description", validators=[DataRequired(), Length(min=20, max=2000)]
    )

    def validate_application_deadline(self, field):
        if field.data and field.data <= datetime.now().date():
            raise ValidationError("Deadline must be a future date.")
