#!/usr/bin/env python3
"""
Crab Grass Knowledge Base

This module provides comprehensive information about crab grass identification,
treatment options, and prevention strategies for lawn care management.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, NamedTuple, Optional
from lawn_care_calculator import Region, Season, TimingWindow


class CrabGrassStage(Enum):
    SEED = "seed"
    GERMINATION = "germination" 
    SEEDLING = "seedling"
    MATURE = "mature"
    SEED_PRODUCTION = "seed_production"


class TreatmentType(Enum):
    PRE_EMERGENT = "pre_emergent"
    POST_EMERGENT = "post_emergent"
    MECHANICAL = "mechanical"
    CULTURAL = "cultural"
    ORGANIC = "organic"


class CrabGrassType(Enum):
    LARGE = "large_crabgrass"
    SMOOTH = "smooth_crabgrass"


class IdentificationFeature(NamedTuple):
    feature: str
    description: str
    distinguishing_characteristics: str


class Treatment(NamedTuple):
    name: str
    type: TreatmentType
    effectiveness: int  # 1-10 scale
    timing: TimingWindow
    application_notes: str
    cost_range: str


class CrabGrassKnowledgeBase:
    """Comprehensive knowledge base for crab grass identification and treatment."""
    
    def __init__(self, region: Region = Region.CENTRAL):
        self.region = region
        self._identification_features = self._initialize_identification_features()
        self._treatments = self._initialize_treatments()
        self._lifecycle_info = self._initialize_lifecycle_info()
        self._prevention_strategies = self._initialize_prevention_strategies()
    
    def _initialize_identification_features(self) -> Dict[CrabGrassType, List[IdentificationFeature]]:
        """Initialize identification features for different crab grass types."""
        return {
            CrabGrassType.LARGE: [
                IdentificationFeature(
                    "Leaf blade", 
                    "Wide, flat leaves 4-8mm wide",
                    "Broader than smooth crabgrass, with visible veins"
                ),
                IdentificationFeature(
                    "Growth pattern",
                    "Low-growing, spreading in star pattern",
                    "Forms mats that can spread 2+ feet in diameter"
                ),
                IdentificationFeature(
                    "Stem",
                    "Thick, jointed stems that root at nodes",
                    "Often reddish at base, can root wherever nodes touch soil"
                ),
                IdentificationFeature(
                    "Seed head",
                    "4-10 finger-like spikes radiating from stem tip",
                    "Purple-tinged when mature, arranged like fingers on a hand"
                ),
                IdentificationFeature(
                    "Height",
                    "Can grow 6-24 inches tall",
                    "Taller than smooth crabgrass when upright"
                )
            ],
            CrabGrassType.SMOOTH: [
                IdentificationFeature(
                    "Leaf blade",
                    "Narrow leaves 2-5mm wide",
                    "Narrower and more pointed than large crabgrass"
                ),
                IdentificationFeature(
                    "Growth pattern", 
                    "Low, prostrate growth forming dense mats",
                    "Stays closer to ground, forms tight carpets"
                ),
                IdentificationFeature(
                    "Stem",
                    "Thinner, smooth stems",
                    "Less robust than large crabgrass, lighter colored"
                ),
                IdentificationFeature(
                    "Seed head",
                    "3-6 narrow spikes, more delicate appearance",
                    "Smaller and more refined than large crabgrass"
                ),
                IdentificationFeature(
                    "Texture",
                    "Smooth leaves without hair",
                    "Distinguishes from hairy crabgrass varieties"
                )
            ]
        }
    
    def _initialize_treatments(self) -> Dict[Region, List[Treatment]]:
        """Initialize treatment options by region."""
        return {
            Region.NORTHERN: [
                Treatment(
                    "Pre-emergent herbicide (Prodiamine)",
                    TreatmentType.PRE_EMERGENT,
                    9,
                    TimingWindow(3, 4, 50, 65, "Apply when soil temperature reaches 55°F"),
                    "Apply before forsythia blooms. Water in within 7 days.",
                    "$30-60 per application"
                ),
                Treatment(
                    "Pre-emergent herbicide (Dithiopyr)", 
                    TreatmentType.PRE_EMERGENT,
                    8,
                    TimingWindow(3, 4, 50, 65, "Early spring application"),
                    "Can provide some post-emergent control on young seedlings.",
                    "$40-70 per application"
                ),
                Treatment(
                    "Post-emergent herbicide (Quinclorac)",
                    TreatmentType.POST_EMERGENT,
                    7,
                    TimingWindow(5, 8, 60, 85, "Apply to young plants before seed production"),
                    "Most effective on plants less than 4 inches. May require multiple applications.",
                    "$25-50 per application"
                ),
                Treatment(
                    "Hand pulling",
                    TreatmentType.MECHANICAL,
                    6,
                    TimingWindow(5, 9, 60, 85, "Remove before seed production"),
                    "Most effective after rain when soil is moist. Remove entire root system.",
                    "Free (labor only)"
                ),
                Treatment(
                    "Corn gluten meal",
                    TreatmentType.ORGANIC,
                    5,
                    TimingWindow(3, 4, 50, 65, "Apply 4-6 weeks before germination"),
                    "Acts as pre-emergent. Apply at 20 lbs per 1000 sq ft.",
                    "$40-80 per application"
                )
            ],
            Region.CENTRAL: [
                Treatment(
                    "Pre-emergent herbicide (Prodiamine)",
                    TreatmentType.PRE_EMERGENT,
                    9,
                    TimingWindow(2, 4, 45, 65, "Apply when soil temperature reaches 50°F"),
                    "Critical timing - apply before soil reaches 55°F consistently.",
                    "$30-60 per application"
                ),
                Treatment(
                    "Split pre-emergent application",
                    TreatmentType.PRE_EMERGENT,
                    8,
                    TimingWindow(2, 3, 45, 60, "Early spring, follow-up in late spring"),
                    "Apply 60% in early spring, 40% 6-8 weeks later.",
                    "$50-90 per season"
                ),
                Treatment(
                    "Post-emergent selective (Fenoxaprop)",
                    TreatmentType.POST_EMERGENT,
                    7,
                    TimingWindow(4, 9, 60, 90, "Apply to actively growing young plants"),
                    "Safe for most cool-season grasses. Apply with surfactant.",
                    "$35-60 per application"
                ),
                Treatment(
                    "Dense lawn maintenance",
                    TreatmentType.CULTURAL,
                    8,
                    TimingWindow(3, 11, 50, 90, "Year-round thick lawn strategy"),
                    "Maintain thick, healthy turf. Overseed thin areas in fall.",
                    "$100-200 per season"
                ),
                Treatment(
                    "Mechanical removal + overseeding",
                    TreatmentType.MECHANICAL,
                    6,
                    TimingWindow(8, 9, 60, 80, "Remove in summer, overseed in fall"),
                    "Pull crabgrass, immediately overseed bare spots with desired grass.",
                    "$50-150 depending on area"
                )
            ],
            Region.SOUTHERN: [
                Treatment(
                    "Pre-emergent herbicide (Atrazine)",
                    TreatmentType.PRE_EMERGENT,
                    8,
                    TimingWindow(1, 3, 40, 65, "Apply before soil temperatures reach 50°F"),
                    "Effective for warm-season grasses. May require earlier application.",
                    "$25-50 per application"
                ),
                Treatment(
                    "Pre-emergent herbicide (Prodiamine)",
                    TreatmentType.PRE_EMERGENT,
                    9,
                    TimingWindow(1, 3, 40, 65, "Very early spring application"),
                    "Apply in late winter. Critical in southern climates.",
                    "$30-60 per application"
                ),
                Treatment(
                    "Post-emergent (MSMA) - where legal",
                    TreatmentType.POST_EMERGENT,
                    8,
                    TimingWindow(3, 10, 65, 95, "Apply to young, actively growing plants"),
                    "Check local regulations. Not allowed in all areas. Highly effective.",
                    "$30-55 per application"
                ),
                Treatment(
                    "Cultural practices (irrigation management)",
                    TreatmentType.CULTURAL,
                    7,
                    TimingWindow(1, 12, 40, 100, "Year-round water management"),
                    "Deep, infrequent watering favors desired grass over crabgrass.",
                    "$0 (management change)"
                ),
                Treatment(
                    "Organic approach (vinegar + salt)",
                    TreatmentType.ORGANIC,
                    4,
                    TimingWindow(4, 10, 70, 95, "Apply to young plants on sunny days"),
                    "20% vinegar solution. Multiple applications needed. May harm desired grass.",
                    "$15-30 per application"
                )
            ]
        }
    
    def _initialize_lifecycle_info(self) -> Dict[CrabGrassStage, Dict[str, str]]:
        """Initialize crab grass lifecycle information."""
        return {
            CrabGrassStage.SEED: {
                "description": "Seeds remain dormant in soil over winter",
                "timing": "Fall through early spring",
                "vulnerability": "Pre-emergent herbicides most effective",
                "identification": "Seeds are small (1-2mm), brownish, not visible in lawn",
                "treatment_window": "Pre-emergent applications before germination"
            },
            CrabGrassStage.GERMINATION: {
                "description": "Seeds begin sprouting when soil temperature reaches 55-60°F",
                "timing": "Late winter to early spring, varies by region",
                "vulnerability": "Last chance for pre-emergent control",
                "identification": "Tiny grass sprouts, difficult to distinguish from desired grass",
                "treatment_window": "Pre-emergent herbicides still effective for 2-3 weeks"
            },
            CrabGrassStage.SEEDLING: {
                "description": "Young plants establish, 1-4 inches tall",
                "timing": "Spring into early summer",
                "vulnerability": "Most susceptible to post-emergent herbicides",
                "identification": "Distinctive wide leaves, low spreading growth pattern",
                "treatment_window": "Optimal time for post-emergent treatment and hand removal"
            },
            CrabGrassStage.MATURE: {
                "description": "Fully developed plants, vigorous growth",
                "timing": "Mid to late summer",
                "vulnerability": "Difficult to control, resistant to many herbicides",
                "identification": "Large mats, distinctive seed heads, choking out desired grass",
                "treatment_window": "Mechanical removal, prepare for next year's prevention"
            },
            CrabGrassStage.SEED_PRODUCTION: {
                "description": "Plants produce thousands of seeds per plant",
                "timing": "Late summer through fall",
                "vulnerability": "Focus on preventing seed spread",
                "identification": "Prominent finger-like seed heads, plants turning brown",
                "treatment_window": "Remove seed heads, plan next year's pre-emergent program"
            }
        }
    
    def _initialize_prevention_strategies(self) -> List[Dict[str, str]]:
        """Initialize prevention strategies."""
        return [
            {
                "strategy": "Maintain dense, healthy turf",
                "description": "Thick grass prevents crabgrass establishment",
                "implementation": "Regular fertilization, proper watering, overseeding thin areas",
                "effectiveness": "High - prevents 70-90% of crabgrass problems"
            },
            {
                "strategy": "Proper mowing height",
                "description": "Taller grass shades soil, preventing crabgrass germination", 
                "implementation": "Mow cool-season grass 2.5-3.5 inches, warm-season 1-2.5 inches",
                "effectiveness": "Medium - reduces germination by 40-60%"
            },
            {
                "strategy": "Pre-emergent herbicide program",
                "description": "Prevent seeds from germinating in spring",
                "implementation": "Apply when forsythia blooms or soil reaches 55°F",
                "effectiveness": "Very High - 85-95% control when properly timed"
            },
            {
                "strategy": "Irrigation management", 
                "description": "Deep, infrequent watering favors desired grass",
                "implementation": "Water 1-1.5 inches per week in 2-3 sessions",
                "effectiveness": "Medium - supports overall turf health"
            },
            {
                "strategy": "Fall overseeding",
                "description": "Thicken lawn before next growing season",
                "implementation": "Overseed thin areas in late summer/early fall",
                "effectiveness": "High - establishes competition for next year"
            },
            {
                "strategy": "Soil health improvement",
                "description": "Healthy soil supports strong turf grass",
                "implementation": "Annual soil testing, pH adjustment, organic matter addition",
                "effectiveness": "Medium-High - long-term turf improvement"
            }
        ]
    
    def identify_crab_grass(self, observed_features: List[str]) -> Dict[str, any]:
        """Identify crab grass type based on observed features."""
        scores = {grass_type: 0 for grass_type in CrabGrassType}
        matches = {grass_type: [] for grass_type in CrabGrassType}
        
        for grass_type, features in self._identification_features.items():
            for feature in features:
                for observed in observed_features:
                    if observed.lower() in feature.description.lower() or \
                       observed.lower() in feature.distinguishing_characteristics.lower():
                        scores[grass_type] += 1
                        matches[grass_type].append(feature)
        
        # Determine most likely type
        if scores[CrabGrassType.LARGE] == scores[CrabGrassType.SMOOTH] == 0:
            likely_type = None
            confidence = "Unable to identify"
        elif scores[CrabGrassType.LARGE] > scores[CrabGrassType.SMOOTH]:
            likely_type = CrabGrassType.LARGE
            confidence = "High" if scores[CrabGrassType.LARGE] >= 3 else "Medium"
        elif scores[CrabGrassType.SMOOTH] > scores[CrabGrassType.LARGE]:
            likely_type = CrabGrassType.SMOOTH
            confidence = "High" if scores[CrabGrassType.SMOOTH] >= 3 else "Medium"
        else:
            likely_type = "Uncertain - could be either type"
            confidence = "Low"
        
        return {
            "likely_type": likely_type.value if hasattr(likely_type, 'value') else str(likely_type),
            "confidence": confidence,
            "matching_features": {grass_type.value: [f.feature for f in features] 
                                for grass_type, features in matches.items() if features},
            "scores": {grass_type.value: score for grass_type, score in scores.items()}
        }
    
    def get_identification_guide(self) -> Dict[str, List[Dict[str, str]]]:
        """Get comprehensive identification guide."""
        guide = {}
        for grass_type, features in self._identification_features.items():
            guide[grass_type.value] = [
                {
                    "feature": feature.feature,
                    "description": feature.description,
                    "distinguishing_characteristics": feature.distinguishing_characteristics
                }
                for feature in features
            ]
        return guide
    
    def get_treatment_recommendations(self, current_month: int, 
                                   crab_grass_stage: Optional[CrabGrassStage] = None) -> List[Dict]:
        """Get treatment recommendations based on timing and stage."""
        if crab_grass_stage is None:
            # Determine likely stage based on month
            if current_month in [12, 1, 2]:
                crab_grass_stage = CrabGrassStage.SEED
            elif current_month in [3, 4]:
                crab_grass_stage = CrabGrassStage.GERMINATION
            elif current_month in [5, 6]:
                crab_grass_stage = CrabGrassStage.SEEDLING
            elif current_month in [7, 8]:
                crab_grass_stage = CrabGrassStage.MATURE
            else:
                crab_grass_stage = CrabGrassStage.SEED_PRODUCTION
        
        treatments = self._treatments.get(self.region, [])
        suitable_treatments = []
        
        for treatment in treatments:
            # Check if treatment timing matches current month
            timing = treatment.timing
            if timing.start_month <= timing.end_month:
                month_match = timing.start_month <= current_month <= timing.end_month
            else:
                month_match = current_month >= timing.start_month or current_month <= timing.end_month
            
            # Check if treatment type is appropriate for stage
            stage_appropriate = False
            if crab_grass_stage in [CrabGrassStage.SEED, CrabGrassStage.GERMINATION]:
                stage_appropriate = treatment.type in [TreatmentType.PRE_EMERGENT, TreatmentType.CULTURAL]
            elif crab_grass_stage == CrabGrassStage.SEEDLING:
                stage_appropriate = treatment.type in [TreatmentType.POST_EMERGENT, TreatmentType.MECHANICAL, 
                                                     TreatmentType.ORGANIC]
            elif crab_grass_stage in [CrabGrassStage.MATURE, CrabGrassStage.SEED_PRODUCTION]:
                stage_appropriate = treatment.type in [TreatmentType.MECHANICAL, TreatmentType.CULTURAL]
            
            if month_match or stage_appropriate:
                suitable_treatments.append({
                    "name": treatment.name,
                    "type": treatment.type.value,
                    "effectiveness": treatment.effectiveness,
                    "timing": f"Months {timing.start_month}-{timing.end_month}",
                    "temperature_range": f"{timing.optimal_temp_min}°F-{timing.optimal_temp_max}°F",
                    "application_notes": treatment.application_notes,
                    "cost_range": treatment.cost_range,
                    "timing_match": month_match,
                    "stage_appropriate": stage_appropriate
                })
        
        # Sort by effectiveness and timing appropriateness
        suitable_treatments.sort(key=lambda x: (x["timing_match"], x["stage_appropriate"], x["effectiveness"]), 
                               reverse=True)
        
        return suitable_treatments
    
    def get_lifecycle_info(self, stage: Optional[CrabGrassStage] = None) -> Dict:
        """Get lifecycle information for a specific stage or all stages."""
        if stage:
            return {stage.value: self._lifecycle_info[stage]}
        return {stage.value: info for stage, info in self._lifecycle_info.items()}
    
    def get_prevention_strategies(self) -> List[Dict[str, str]]:
        """Get comprehensive prevention strategies."""
        return self._prevention_strategies.copy()
    
    def get_seasonal_calendar(self) -> Dict[str, List[str]]:
        """Get seasonal crab grass management calendar."""
        calendar = {
            "Late Winter (Jan-Feb)": [
                "Plan pre-emergent herbicide application",
                "Order pre-emergent products",
                "Assess lawn for thin areas needing attention",
                "Soil test if not done in fall"
            ],
            "Early Spring (Mar-Apr)": [
                "Apply pre-emergent herbicide when forsythia blooms",
                "Fertilize existing grass to promote thick growth", 
                "Begin regular mowing at proper height",
                "Water lawn deeply but infrequently"
            ],
            "Late Spring (May-Jun)": [
                "Monitor for crabgrass seedlings",
                "Apply post-emergent herbicide if needed",
                "Hand-pull small patches of young crabgrass",
                "Continue proper watering and mowing practices"
            ],
            "Summer (Jul-Aug)": [
                "Hand-pull mature crabgrass before seed production",
                "Focus on lawn care practices that favor desired grass",
                "Plan fall overseeding for thin areas",
                "Monitor and remove seed heads if present"
            ],
            "Fall (Sep-Nov)": [
                "Overseed thin areas to prevent next year's crabgrass",
                "Apply fall fertilizer to strengthen grass",
                "Remove any remaining crabgrass plants",
                "Plan next year's pre-emergent program"
            ]
        }
        return calendar
    
    def diagnose_control_failure(self, treatment_applied: str, 
                                application_month: int, 
                                current_crabgrass_level: str) -> Dict[str, any]:
        """Diagnose why crab grass control may have failed."""
        possible_causes = []
        recommendations = []
        
        # Analyze timing issues
        if "pre-emergent" in treatment_applied.lower():
            if application_month > 4:  # Too late for most regions
                possible_causes.append("Pre-emergent applied too late in season")
                recommendations.append("Apply pre-emergent earlier next year (when forsythia blooms)")
            
            if current_crabgrass_level == "high":
                possible_causes.append("Pre-emergent may have broken down or washed away")
                recommendations.append("Consider split application or longer-lasting product")
        
        if "post-emergent" in treatment_applied.lower():
            if current_crabgrass_level == "high":
                possible_causes.append("Post-emergent applied too late (mature plants resistant)")
                recommendations.append("Target younger, smaller plants for better control")
        
        # General causes
        possible_causes.extend([
            "Inadequate application rate or coverage",
            "Weather conditions (too much rain, drought, extreme temperatures)",
            "Dense crabgrass population overwhelming treatment",
            "Poor lawn health allowing crabgrass establishment",
            "Seed bank from previous years still germinating"
        ])
        
        recommendations.extend([
            "Improve overall lawn density through fertilization and overseeding",
            "Ensure proper application timing and rates",
            "Consider professional soil test and lawn analysis",
            "Plan integrated approach combining multiple treatment methods"
        ])
        
        return {
            "treatment_applied": treatment_applied,
            "application_timing": f"Month {application_month}",
            "current_level": current_crabgrass_level,
            "possible_causes": possible_causes,
            "recommendations": recommendations,
            "next_steps": "Focus on fall lawn thickening and plan comprehensive approach for next year"
        }


def main():
    """Demo the crab grass knowledge base functionality."""
    kb = CrabGrassKnowledgeBase(Region.CENTRAL)
    
    print("Crab Grass Knowledge Base")
    print("=" * 50)
    
    # Identification guide
    print("\nIdentification Guide:")
    print("-" * 30)
    guide = kb.get_identification_guide()
    for grass_type, features in guide.items():
        print(f"\n{grass_type.replace('_', ' ').title()}:")
        for feature in features:
            print(f"  {feature['feature']}: {feature['description']}")
    
    # Current month treatments
    current_month = datetime.now().month
    print(f"\nRecommended Treatments for Month {current_month}:")
    print("-" * 40)
    treatments = kb.get_treatment_recommendations(current_month)
    for i, treatment in enumerate(treatments[:3], 1):  # Show top 3
        print(f"\n{i}. {treatment['name']}")
        print(f"   Effectiveness: {treatment['effectiveness']}/10")
        print(f"   Type: {treatment['type'].replace('_', ' ').title()}")
        print(f"   Cost: {treatment['cost_range']}")
        print(f"   Notes: {treatment['application_notes']}")
    
    # Prevention strategies
    print(f"\nPrevention Strategies:")
    print("-" * 30)
    strategies = kb.get_prevention_strategies()
    for strategy in strategies[:3]:  # Show top 3
        print(f"\n• {strategy['strategy']}")
        print(f"  {strategy['description']}")
        print(f"  Effectiveness: {strategy['effectiveness']}")


if __name__ == "__main__":
    main()