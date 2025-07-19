"""
Practice Areas Module for Ted Sink Law

Defines all personal injury case types that Ted Sink Law handles,
as well as case types they do not accept.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class CaseCategory(Enum):
    """Categories of personal injury cases"""
    MOTOR_VEHICLE = "motor_vehicle"
    WORKPLACE = "workplace"
    PREMISES_LIABILITY = "premises_liability"
    MEDICAL = "medical"
    WRONGFUL_DEATH = "wrongful_death"
    OTHER_PERSONAL_INJURY = "other_personal_injury"

@dataclass
class PracticeArea:
    """Represents a practice area/case type"""
    name: str
    category: CaseCategory
    description: str
    keywords: List[str]
    is_handled: bool = True
    priority_level: int = 1  # 1 = high priority, 2 = medium, 3 = low

class TedSinkLawPracticeAreas:
    """Practice areas and case types for Ted Sink Law"""
    
    # PERSONAL INJURY CASES - HANDLED
    PERSONAL_INJURY_CASES = [
        PracticeArea(
            name="Car Accidents",
            category=CaseCategory.MOTOR_VEHICLE,
            description="Automobile collision cases including rear-end, side-impact, and head-on collisions",
            keywords=["car accident", "auto accident", "vehicle collision", "car crash", "automobile accident"],
            priority_level=1
        ),
        PracticeArea(
            name="Truck Accidents",
            category=CaseCategory.MOTOR_VEHICLE,
            description="Commercial truck and semi-truck accident cases",
            keywords=["truck accident", "semi-truck", "commercial truck", "18-wheeler", "big rig"],
            priority_level=1
        ),
        PracticeArea(
            name="Motorcycle Accidents",
            category=CaseCategory.MOTOR_VEHICLE,
            description="Motorcycle collision and injury cases",
            keywords=["motorcycle accident", "bike accident", "motorcycle crash", "motorcycle injury"],
            priority_level=1
        ),
        PracticeArea(
            name="Workers' Compensation",
            category=CaseCategory.WORKPLACE,
            description="Workplace injury and workers' compensation claims",
            keywords=["workers comp", "workers compensation", "workplace injury", "on-the-job injury", "work injury"],
            priority_level=1
        ),
        PracticeArea(
            name="Wrongful Death",
            category=CaseCategory.WRONGFUL_DEATH,
            description="Wrongful death claims due to negligence or intentional acts",
            keywords=["wrongful death", "fatal accident", "death claim", "survival action"],
            priority_level=1
        ),
        PracticeArea(
            name="Premises Liability",
            category=CaseCategory.PREMISES_LIABILITY,
            description="Injuries on someone else's property due to unsafe conditions",
            keywords=["premises liability", "slip and fall", "unsafe property", "property injury"],
            priority_level=2
        ),
        PracticeArea(
            name="Ride-Share Accidents",
            category=CaseCategory.MOTOR_VEHICLE,
            description="Accidents involving Uber, Lyft, and other ride-sharing services",
            keywords=["uber accident", "lyft accident", "ride share", "rideshare accident"],
            priority_level=2
        ),
        PracticeArea(
            name="Medical Malpractice",
            category=CaseCategory.MEDICAL,
            description="Medical negligence and malpractice cases",
            keywords=["medical malpractice", "medical negligence", "doctor error", "hospital error"],
            priority_level=2
        ),
        PracticeArea(
            name="Nursing Home Abuse",
            category=CaseCategory.MEDICAL,
            description="Nursing home neglect and abuse cases",
            keywords=["nursing home abuse", "nursing home neglect", "elder abuse", "assisted living abuse"],
            priority_level=2
        ),
        PracticeArea(
            name="Slip and Fall",
            category=CaseCategory.PREMISES_LIABILITY,
            description="Slip, trip, and fall injury cases",
            keywords=["slip and fall", "trip and fall", "fall accident", "slip injury"],
            priority_level=2
        ),
        PracticeArea(
            name="Construction Accidents",
            category=CaseCategory.WORKPLACE,
            description="Construction site injuries and accidents",
            keywords=["construction accident", "construction injury", "construction site", "workplace construction"],
            priority_level=2
        ),
        PracticeArea(
            name="Pedestrian Accidents",
            category=CaseCategory.MOTOR_VEHICLE,
            description="Pedestrian struck by vehicle cases",
            keywords=["pedestrian accident", "hit by car", "walking accident", "crossing accident"],
            priority_level=2
        ),
        PracticeArea(
            name="Bicycle Accidents",
            category=CaseCategory.MOTOR_VEHICLE,
            description="Bicycle collision and injury cases",
            keywords=["bicycle accident", "bike accident", "cycling accident", "bike crash"],
            priority_level=3
        ),
        PracticeArea(
            name="Dog Bites",
            category=CaseCategory.OTHER_PERSONAL_INJURY,
            description="Dog bite and animal attack cases",
            keywords=["dog bite", "animal attack", "pet injury", "dog attack"],
            priority_level=3
        ),
        PracticeArea(
            name="Product Liability",
            category=CaseCategory.OTHER_PERSONAL_INJURY,
            description="Defective product injury cases",
            keywords=["product liability", "defective product", "product injury", "unsafe product"],
            priority_level=3
        )
    ]
    
    # CASE TYPES NOT HANDLED
    NON_PERSONAL_INJURY_CASES = [
        PracticeArea(
            name="Criminal Defense",
            category=CaseCategory.OTHER_PERSONAL_INJURY,
            description="Criminal cases and defense",
            keywords=["criminal", "criminal defense", "arrest", "charges", "criminal case"],
            is_handled=False
        ),
        PracticeArea(
            name="Family Law",
            category=CaseCategory.OTHER_PERSONAL_INJURY,
            description="Divorce, custody, and family law matters",
            keywords=["divorce", "custody", "family law", "child support", "alimony"],
            is_handled=False
        ),
        PracticeArea(
            name="Business Law",
            category=CaseCategory.OTHER_PERSONAL_INJURY,
            description="Business formation, contracts, and corporate law",
            keywords=["business law", "corporate", "contracts", "business formation", "LLC"],
            is_handled=False
        ),
        PracticeArea(
            name="Real Estate",
            category=CaseCategory.OTHER_PERSONAL_INJURY,
            description="Real estate transactions and property law",
            keywords=["real estate", "property law", "closing", "title", "mortgage"],
            is_handled=False
        ),
        PracticeArea(
            name="Estate Planning",
            category=CaseCategory.OTHER_PERSONAL_INJURY,
            description="Wills, trusts, and estate planning",
            keywords=["estate planning", "will", "trust", "probate", "inheritance"],
            is_handled=False
        ),
        PracticeArea(
            name="Bankruptcy",
            category=CaseCategory.OTHER_PERSONAL_INJURY,
            description="Bankruptcy and debt relief",
            keywords=["bankruptcy", "debt relief", "chapter 7", "chapter 13", "foreclosure"],
            is_handled=False
        )
    ]
    
    @classmethod
    def get_all_practice_areas(cls) -> List[PracticeArea]:
        """Get all practice areas (both handled and not handled)"""
        return cls.PERSONAL_INJURY_CASES + cls.NON_PERSONAL_INJURY_CASES
    
    @classmethod
    def get_handled_practice_areas(cls) -> List[PracticeArea]:
        """Get only practice areas that Ted Sink Law handles"""
        return [area for area in cls.PERSONAL_INJURY_CASES if area.is_handled]
    
    @classmethod
    def get_non_handled_practice_areas(cls) -> List[PracticeArea]:
        """Get practice areas that Ted Sink Law does not handle"""
        return cls.NON_PERSONAL_INJURY_CASES
    
    @classmethod
    def find_practice_area_by_keyword(cls, keyword: str) -> Optional[PracticeArea]:
        """Find a practice area by keyword"""
        keyword_lower = keyword.lower()
        for area in cls.get_all_practice_areas():
            if keyword_lower in [k.lower() for k in area.keywords]:
                return area
        return None
    
    @classmethod
    def is_personal_injury_case(cls, case_description: str) -> bool:
        """Check if a case description matches personal injury practice areas"""
        case_lower = case_description.lower()
        for area in cls.get_handled_practice_areas():
            if any(keyword.lower() in case_lower for keyword in area.keywords):
                return True
        return False
    
    @classmethod
    def is_non_personal_injury_case(cls, case_description: str) -> bool:
        """Check if a case description matches non-personal injury practice areas"""
        case_lower = case_description.lower()
        for area in cls.get_non_handled_practice_areas():
            if any(keyword.lower() in case_lower for keyword in area.keywords):
                return True
        return False
    
    @classmethod
    def get_high_priority_cases(cls) -> List[PracticeArea]:
        """Get high priority personal injury cases"""
        return [area for area in cls.get_handled_practice_areas() if area.priority_level == 1]
    
    @classmethod
    def get_case_categories(cls) -> List[CaseCategory]:
        """Get all case categories"""
        return list(CaseCategory)
    
    @classmethod
    def get_cases_by_category(cls, category: CaseCategory) -> List[PracticeArea]:
        """Get all cases in a specific category"""
        return [area for area in cls.get_handled_practice_areas() if area.category == category]