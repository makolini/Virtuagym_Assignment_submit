"""
The Lead entity:

Imagine you're tasked with helping a gym manager who wants to better understand 
and track potential customers—leads—and see how well these leads convert into 
members. As you think about how to support this goal, consider the first step: 
defining the structure of a Lead.

Think how a lead transform to a member. What data should be captured to represent 
this entity comprehensively? Think beyond basic attributes and consider what 
information would help the gym manager track a leads journey from creation to 
conversion.

Answer: 
A lead is a potential customer who has shown interest in the gym's services but 
has not yet become a member. Leads are like seeds that need nurturing and tracking to grow into a tree - a customer. 
To represent a lead comprehensively, we need to capture atleast the following data:
  - Name
  - Email
  - Phone Number
  - Address
  - Date of Birth
  - Gender
  - Status # new, interested, trial, converted, lost... 
  - Employment # working, student, unemployed, etc.
  - Source # how did they hear about the gym? (friend, website, social media, etc.)
  - Notes # any additional information about the lead
  - Fitness Level # beginner, intermediate, advanced
  - Fitness Goals # weight loss, muscle gain, etc.
  - Fitness Experience # gym goer, runner, yogi, etc.
  - Fitness Frequency # daily, weekly, monthly, etc.


[EXTRA] Coding Insight : Taking this a step further, think about how you
would represent the Lead entity using object-oriented programming
(OOP). Create a simple class structure to illustrate how this could be
done. You can use pseudocode or a language of your choice.
"""

# dataclasses: Automatically generates __init__, __repr__, __eq__ methods
# Reduces boilerplate code and makes class definitions more concise
from dataclasses import dataclass

# datetime.date: Provides proper date handling with validation
# Better than using strings or timestamps for birth dates
from datetime import date

# enum: Creates enumerated types for constrained choices
# Safer than using strings/constants, provides type checking
from enum import Enum

# typing: Enables static type hints for better code clarity and IDE support
# List and Optional are generic types that make code more maintainable
from typing import List, Optional

# uuid: Generates universally unique identifiers
# UUID is the type annotation, uuid4() is the generator function
# Better than auto-increment IDs for distributed systems
from uuid import UUID, uuid4

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Employment(Enum):
    WORKING = "working"
    STUDENT = "student"
    UNEMPLOYED = "unemployed"

class LeadStatus(Enum): # example statuses, in the end I implemented only NEW, CONTACTED, CONVERTED.
    NEW = "new"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    TRIAL = "trial"
    NEGOTIATING = "negotiating"
    CONVERTED = "converted"
    LOST = "lost"

class LeadSource(Enum): # example sources
    WEBSITE = "website"
    FRIEND = "friend"
    REFERRAL = "referral"
    WALK_IN = "walk_in"
    SOCIAL_MEDIA = "social_media"
    ADVERTISEMENT = "advertisement"
    OTHER = "other"

class FitnessLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class Address:
    street: str
    city: str
    postal_code: str
    country: str

class Lead:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: Address,
        creation_date: date,
        date_of_birth: date,
        gender: Gender,
        employment: Employment,
        status: LeadStatus = LeadStatus.NEW, # default to new
        source: LeadSource = LeadSource.WALK_IN, # default to walk in
        notes: Optional[str] = None,
        fitness_level: FitnessLevel = FitnessLevel.BEGINNER, # default to beginner
        fitness_goals: Optional[List[str]] = None,
        fitness_frequency: Optional[int] = None,
        staff_id: Optional[UUID] = None,
        club_id: Optional[UUID] = None,
        last_contact: Optional[date] = None,
    ):
        self.id: UUID = uuid4() # guaranteed to be unique, without the need to validate
        self.first_name = first_name
        self.last_name = last_name
        self.email = email # may require validation
        self.phone = phone # may require validation
        self.address = address
        self.creation_date = creation_date
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.employment = employment
        self.status = status
        self.source = source
        self.notes = notes
        self.fitness_level = fitness_level
        self.fitness_goals = fitness_goals
        self.fitness_frequency = fitness_frequency
        self.staff_id = staff_id
        self.club_id = club_id
        self.last_contact = last_contact
        self.last_updated = date.today()

"""
Data modeling - Lead, Staff, Club, Subscription, Subscription_type.
Conceptual data modeling - Entity-Relationship (ER) diagram.
Idea for data modeling:
  - (already done)Lead: A potential customer who has shown interest in the gym's services but has not yet become a member.
  - Staff: Gym staff members who work at the gym.
  - Club: A physical location where the gym operates, houses other entities.
  - Member (converted lead): A customer who has become a member of the gym = converted Lead. Possibly unnecessary table.
  - Subscription: A contract between the gym and a converted lead, outlining the terms of the membership, includes payment information.
  - Subscription_type: A type of subscription. E.g. has duration, base price, name, decsription...
"""
class Club:
    def __init__(self, name: str, address: Address, capacity: int, operating_hours: str, established_date: date, monthly_target: int, revenue: float):
        self.id: UUID = uuid4()
        self.name = name
        self.address = address
        self.capacity = capacity
        self.operating_hours = operating_hours
        self.established_date = established_date
        self.monthly_target = monthly_target
        self.revenue = revenue
class Staff:
    def __init__(self, first_name: str, last_name: str, role: str, hire_date: date, email: str, phone: str, club_id: UUID):
        self.id: UUID = uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.role = role # (trainer, sales, manager...)
        self.hire_date = hire_date
        self.email = email
        self.phone = phone
        self.club_id = club_id
        # KPI calculation
        # to calculate KPI: retrieve leads and converted leads from "lead" table that belong to this staff member
        # then calculate the conversion rate
        # e.g.:
        """
        converted_leads = SELECT COUNT(*) FROM lead WHERE staff_id = self.id AND status = 'converted';
        total_leads = SELECT COUNT(*) FROM lead WHERE staff_id = self.id;
        conversion_rate = (converted_leads / total_leads) * 100
        """
# Class Member
"""
    A member is a converted lead. Second table for a member may not be necessary.
    However, it may be useful for tracking the member's progress and additional data, which do not make sense to be in the lead table.
    Therefore, the member table would only contain any extra data that is not needed in the lead table.
    I have decided to not create a separate table for a member, but rather make use of the lead table and subscription table to store necessary data.
"""
class Subscription:
    def __init__(self, type_id: UUID,
                  actual_price: float, 
                  lead_id: UUID, 
                  start_date: date, 
                  end_date: date, 
                  last_visit: date, 
                  visits: int, 
                  payment_status: str, 
                  billing_cycle: str, 
                  auto_renewal: bool, 
                  active: bool):
        self.id: UUID = uuid4()
        self.type_id = type_id
        self.actual_price = actual_price
        self.lead_id = lead_id
        self.start_date = start_date
        self.end_date = end_date
        self.last_visit = last_visit
        self.visits = visits
        self.payment_status = payment_status
        self.billing_cycle = billing_cycle
        self.auto_renewal = auto_renewal
        self.active = active
class Subscription_type:
    def __init__(self, name: str, description: str, base_price: float, duration: int):
        self.id: UUID = uuid4()
        self.name = name
        self.description = description
        self.base_price = base_price
        self.duration = duration # 30 days, 60 days, 90 days, etc.
"""
Tracking Key Dates : In the world of lead management, time is crucial. A lead
has a creation_date , marking when it first appears, and a conversion_date,
showing when it turns into a paying member. Think about how these dates
can be used to develop insightful metrics.
a. When would the creation_date be more relevant, and when would
the conversion_date provide the most value?
b. How does the Staff entity interact with the conversion_date to track
their effectiveness?

Answer:
a. The creation_date would be more relevant when tracking the lead's journey from creation to conversion.
    It would be relevant when tracking staff KPIs, and to know which lead to give priority to (e.g. new leads).
b. The conversion_date would provide the most value when tracking members.
    As the conversion_date is the date when the lead becomes a member and takes out a subscription.
"""

"""
Building the Database: gym_assignment.sqlite
"""

"""
A Manager’s View: Creating a Dashboard: Now that you’ve defined the
structure and relationships between key entities, it’s time to bring the data to
life through visualizations. Design a dashboard that a gym manager could use
to track lead conversion performance and staff contributions. Think creatively
about what metrics and interactive elements would help them explore this
data effectively. Make sure to put yourself into the manager’s role and think of
what are the metrics that they care the most. What kind of filters or drill-down
capabilities might they appreciate? Sketch your dashboard and explain the
choices behind your visual elements. Note: No need to actually build the
dashboard, you can simply design the ideal end-result.:
https://ynbqytlipllwwkjx.vercel.app
"""
"""
Querying the Database : Write a SQL query for each of the following
questions: (I had difficulty replicating the exact example, because my database has a slightly different structure.)
    
    This query shows the revenue generated by each staff member, and the conversion rate for each month:
SELECT 
    staff.first_name,
    strftime('%Y-%m', lead.converted_date) as month,
    SUM(subscription.actual_price) as month_revenue,
    COUNT(*) as total_leads,
    COUNT(CASE WHEN lead.status = 'Converted' THEN 1 END) as conversions,
    ROUND(COUNT(CASE WHEN lead.status = 'Converted' THEN 1 END) * 100.0 / COUNT(*), 2) as conversion_rate
FROM staff
JOIN lead ON staff.staff_id = lead.staff_id
LEFT JOIN subscription ON lead.lead_id = subscription.lead_id
WHERE lead.converted_date >= date('now', '-3 months')
GROUP BY 
    staff.staff_id, 
    staff.first_name, 
    month
ORDER BY 
    month DESC, 
    month_revenue DESC;
"""
"""
Final summary: 
  - Created classes for 5 entitities: Lead, Staff, Club, Subscription, Subscription_type.
  - Created a database for a gym, with a focus on lead management and staff performance tracking, implementing the entitities.
  - Created a dashboard to track lead conversion performance and staff contributions.
  - Queried the database to try to replicate the question in the assignment, but due to difference in database structure, this was not entirely possible.
  - Made use of tools: SQLite - database and SQL query, mockaroo.com - data and database generation, v0.dev - dashboard UI.
"""
