"""
Genetic Disease System for SimuLife
Handles hereditary conditions, disease progression, and genetic health impacts.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum


class DiseaseType(Enum):
    """Types of genetic diseases."""
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    NEUROLOGICAL = "neurological"
    METABOLIC = "metabolic"
    IMMUNE = "immune"
    DEVELOPMENTAL = "developmental"
    MENTAL_HEALTH = "mental_health"
    BLOOD = "blood"
    BONE = "bone"
    SENSORY = "sensory"


class InheritancePattern(Enum):
    """Genetic inheritance patterns."""
    AUTOSOMAL_DOMINANT = "autosomal_dominant"    # One copy needed
    AUTOSOMAL_RECESSIVE = "autosomal_recessive"  # Two copies needed
    X_LINKED = "x_linked"                        # Sex-linked
    POLYGENIC = "polygenic"                      # Multiple genes
    SPORADIC = "sporadic"                        # Random occurrence


class DiseaseSeverity(Enum):
    """Severity levels of genetic diseases."""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


@dataclass
class GeneticDisease:
    """Represents a genetic disease."""
    id: str
    name: str
    disease_type: DiseaseType
    inheritance_pattern: InheritancePattern
    prevalence: float                    # Population frequency (0.0-1.0)
    penetrance: float                   # Expression probability if gene present
    age_of_onset: Tuple[int, int]       # (min_age, max_age)
    severity: DiseaseSeverity
    health_impact: float                # Impact on health per day
    energy_impact: float                # Impact on energy per day
    reproduction_impact: float          # Impact on reproduction ability
    mortality_modifier: float           # Multiplier for death risk
    symptoms: List[str]
    description: str
    treatment_available: bool
    treatment_effectiveness: float      # 0.0-1.0 reduction in impacts


@dataclass
class GeneticCarrier:
    """Represents an agent's genetic disease carrier status."""
    disease_id: str
    copies: int                         # Number of disease copies (0, 1, or 2)
    expressed: bool                     # Whether disease is active
    age_of_onset: Optional[int]         # When disease manifested
    severity: Optional[DiseaseSeverity] # Current severity level
    progression_rate: float             # Disease progression speed
    treatment_status: bool              # Whether receiving treatment


class GeneticDiseaseSystem:
    """
    Manages genetic diseases, inheritance, and health impacts.
    """
    
    def __init__(self):
        self.diseases = self._initialize_diseases()
        self.agent_genetics: Dict[str, Dict[str, GeneticCarrier]] = {}  # agent_id -> disease_id -> carrier_info
        self.disease_statistics = {
            "total_carriers": 0,
            "active_cases": 0,
            "diseases_by_type": {dt.value: 0 for dt in DiseaseType},
            "inheritance_events": [],
            "epidemic_tracking": {}
        }
    
    def _initialize_diseases(self) -> Dict[str, GeneticDisease]:
        """Initialize the genetic disease database."""
        diseases = {}
        
        # Cardiovascular diseases
        diseases["hereditary_heart"] = GeneticDisease(
            id="hereditary_heart",
            name="Hereditary Heart Condition",
            disease_type=DiseaseType.CARDIOVASCULAR,
            inheritance_pattern=InheritancePattern.AUTOSOMAL_DOMINANT,
            prevalence=0.02,
            penetrance=0.8,
            age_of_onset=(30, 60),
            severity=DiseaseSeverity.MODERATE,
            health_impact=0.002,
            energy_impact=0.003,
            reproduction_impact=0.1,
            mortality_modifier=1.5,
            symptoms=["chest pain", "shortness of breath", "fatigue"],
            description="A hereditary condition affecting heart function",
            treatment_available=True,
            treatment_effectiveness=0.6
        )
        
        # Respiratory diseases
        diseases["genetic_asthma"] = GeneticDisease(
            id="genetic_asthma",
            name="Genetic Asthma",
            disease_type=DiseaseType.RESPIRATORY,
            inheritance_pattern=InheritancePattern.POLYGENIC,
            prevalence=0.05,
            penetrance=0.7,
            age_of_onset=(5, 25),
            severity=DiseaseSeverity.MILD,
            health_impact=0.001,
            energy_impact=0.002,
            reproduction_impact=0.05,
            mortality_modifier=1.2,
            symptoms=["wheezing", "coughing", "breathing difficulty"],
            description="Genetic predisposition to respiratory problems",
            treatment_available=True,
            treatment_effectiveness=0.8
        )
        
        # Neurological diseases
        diseases["neural_degeneration"] = GeneticDisease(
            id="neural_degeneration",
            name="Neural Degeneration Syndrome",
            disease_type=DiseaseType.NEUROLOGICAL,
            inheritance_pattern=InheritancePattern.AUTOSOMAL_RECESSIVE,
            prevalence=0.001,
            penetrance=0.95,
            age_of_onset=(40, 70),
            severity=DiseaseSeverity.SEVERE,
            health_impact=0.005,
            energy_impact=0.004,
            reproduction_impact=0.3,
            mortality_modifier=2.0,
            symptoms=["memory loss", "coordination problems", "cognitive decline"],
            description="Progressive neurological deterioration",
            treatment_available=False,
            treatment_effectiveness=0.0
        )
        
        # Metabolic diseases
        diseases["metabolic_disorder"] = GeneticDisease(
            id="metabolic_disorder",
            name="Metabolic Processing Disorder",
            disease_type=DiseaseType.METABOLIC,
            inheritance_pattern=InheritancePattern.AUTOSOMAL_RECESSIVE,
            prevalence=0.008,
            penetrance=0.9,
            age_of_onset=(0, 10),
            severity=DiseaseSeverity.MODERATE,
            health_impact=0.003,
            energy_impact=0.005,
            reproduction_impact=0.2,
            mortality_modifier=1.8,
            symptoms=["growth problems", "weakness", "digestive issues"],
            description="Inability to process certain nutrients properly",
            treatment_available=True,
            treatment_effectiveness=0.7
        )
        
        # Mental health conditions
        diseases["hereditary_depression"] = GeneticDisease(
            id="hereditary_depression",
            name="Hereditary Depression",
            disease_type=DiseaseType.MENTAL_HEALTH,
            inheritance_pattern=InheritancePattern.POLYGENIC,
            prevalence=0.03,
            penetrance=0.6,
            age_of_onset=(15, 40),
            severity=DiseaseSeverity.MODERATE,
            health_impact=0.001,
            energy_impact=0.003,
            reproduction_impact=0.15,
            mortality_modifier=1.3,
            symptoms=["mood changes", "low energy", "social withdrawal"],
            description="Genetic predisposition to depressive episodes",
            treatment_available=True,
            treatment_effectiveness=0.5
        )
        
        # Blood disorders
        diseases["blood_clotting"] = GeneticDisease(
            id="blood_clotting",
            name="Blood Clotting Disorder",
            disease_type=DiseaseType.BLOOD,
            inheritance_pattern=InheritancePattern.X_LINKED,
            prevalence=0.005,
            penetrance=0.85,
            age_of_onset=(0, 20),
            severity=DiseaseSeverity.MODERATE,
            health_impact=0.002,
            energy_impact=0.001,
            reproduction_impact=0.25,
            mortality_modifier=1.6,
            symptoms=["easy bruising", "excessive bleeding", "slow healing"],
            description="Inherited blood clotting deficiency",
            treatment_available=True,
            treatment_effectiveness=0.9
        )
        
        # Bone diseases
        diseases["bone_fragility"] = GeneticDisease(
            id="bone_fragility",
            name="Bone Fragility Syndrome",
            disease_type=DiseaseType.BONE,
            inheritance_pattern=InheritancePattern.AUTOSOMAL_DOMINANT,
            prevalence=0.003,
            penetrance=0.9,
            age_of_onset=(10, 30),
            severity=DiseaseSeverity.MODERATE,
            health_impact=0.002,
            energy_impact=0.002,
            reproduction_impact=0.1,
            mortality_modifier=1.4,
            symptoms=["frequent fractures", "bone pain", "reduced mobility"],
            description="Genetic condition causing weak and brittle bones",
            treatment_available=True,
            treatment_effectiveness=0.4
        )
        
        # Sensory disorders
        diseases["hereditary_blindness"] = GeneticDisease(
            id="hereditary_blindness",
            name="Progressive Vision Loss",
            disease_type=DiseaseType.SENSORY,
            inheritance_pattern=InheritancePattern.AUTOSOMAL_RECESSIVE,
            prevalence=0.001,
            penetrance=0.95,
            age_of_onset=(20, 50),
            severity=DiseaseSeverity.SEVERE,
            health_impact=0.001,
            energy_impact=0.002,
            reproduction_impact=0.05,
            mortality_modifier=1.1,
            symptoms=["vision problems", "night blindness", "complete vision loss"],
            description="Progressive genetic blindness",
            treatment_available=False,
            treatment_effectiveness=0.0
        )
        
        return diseases
    
    def initialize_agent_genetics(self, agent: Any) -> Dict[str, GeneticCarrier]:
        """Initialize genetic profile for a new agent."""
        genetic_profile = {}
        
        for disease_id, disease in self.diseases.items():
            # Determine if agent carries this disease
            carrier_info = self._determine_genetic_status(disease, agent)
            if carrier_info:
                genetic_profile[disease_id] = carrier_info
        
        self.agent_genetics[agent.id] = genetic_profile
        return genetic_profile
    
    def _determine_genetic_status(self, disease: GeneticDisease, agent: Any) -> Optional[GeneticCarrier]:
        """Determine if agent carries a specific genetic disease."""
        # Base probability from disease prevalence
        if random.random() > disease.prevalence:
            return None  # Agent doesn't carry this disease
        
        # Determine number of copies based on inheritance pattern
        copies = self._determine_gene_copies(disease.inheritance_pattern)
        
        if copies == 0:
            return None
        
        # Check if disease is expressed based on inheritance pattern and penetrance
        expressed = self._check_disease_expression(disease, copies)
        
        # Determine age of onset if expressed
        age_of_onset = None
        if expressed:
            min_onset, max_onset = disease.age_of_onset
            age_of_onset = random.randint(min_onset, max_onset)
        
        # Determine progression rate
        progression_rate = random.uniform(0.5, 1.5)
        
        return GeneticCarrier(
            disease_id=disease.id,
            copies=copies,
            expressed=expressed,
            age_of_onset=age_of_onset,
            severity=None,  # Will be determined when disease manifests
            progression_rate=progression_rate,
            treatment_status=False
        )
    
    def _determine_gene_copies(self, inheritance_pattern: InheritancePattern) -> int:
        """Determine number of disease gene copies."""
        if inheritance_pattern == InheritancePattern.AUTOSOMAL_DOMINANT:
            return 1 if random.random() < 0.5 else 0
        elif inheritance_pattern == InheritancePattern.AUTOSOMAL_RECESSIVE:
            # Two independent chances for recessive alleles
            copy1 = 1 if random.random() < 0.1 else 0  # Lower chance for recessive
            copy2 = 1 if random.random() < 0.1 else 0
            return copy1 + copy2
        elif inheritance_pattern == InheritancePattern.X_LINKED:
            return 1 if random.random() < 0.1 else 0  # Sex-linked, simplified
        elif inheritance_pattern == InheritancePattern.POLYGENIC:
            # Multiple genes, simplified as 0-2 risk copies
            return random.randint(0, 2) if random.random() < 0.3 else 0
        elif inheritance_pattern == InheritancePattern.SPORADIC:
            return 1 if random.random() < 0.05 else 0  # Low random chance
        
        return 0
    
    def _check_disease_expression(self, disease: GeneticDisease, copies: int) -> bool:
        """Check if disease is expressed given genetic copies."""
        if copies == 0:
            return False
        
        if disease.inheritance_pattern == InheritancePattern.AUTOSOMAL_DOMINANT:
            return random.random() < disease.penetrance
        elif disease.inheritance_pattern == InheritancePattern.AUTOSOMAL_RECESSIVE:
            if copies >= 2:
                return random.random() < disease.penetrance
            else:
                return False  # Recessive needs 2 copies
        elif disease.inheritance_pattern in [InheritancePattern.X_LINKED, 
                                           InheritancePattern.POLYGENIC, 
                                           InheritancePattern.SPORADIC]:
            return random.random() < disease.penetrance
        
        return False
    
    def inherit_diseases_from_parents(self, child_agent: Any, parent1: Any, parent2: Any) -> Dict[str, GeneticCarrier]:
        """Inherit genetic diseases from parents."""
        child_genetics = {}
        
        parent1_genetics = self.agent_genetics.get(parent1.id, {})
        parent2_genetics = self.agent_genetics.get(parent2.id, {})
        
        # Get all diseases that either parent carries
        all_diseases = set(parent1_genetics.keys()) | set(parent2_genetics.keys())
        
        for disease_id in all_diseases:
            disease = self.diseases[disease_id]
            inherited_status = self._inherit_single_disease(
                disease, parent1_genetics.get(disease_id), parent2_genetics.get(disease_id)
            )
            
            if inherited_status:
                child_genetics[disease_id] = inherited_status
        
        # Check for new random mutations
        for disease_id, disease in self.diseases.items():
            if disease_id not in child_genetics and disease.inheritance_pattern == InheritancePattern.SPORADIC:
                random_carrier = self._determine_genetic_status(disease, child_agent)
                if random_carrier:
                    child_genetics[disease_id] = random_carrier
        
        self.agent_genetics[child_agent.id] = child_genetics
        return child_genetics
    
    def _inherit_single_disease(self, disease: GeneticDisease, 
                               parent1_carrier: Optional[GeneticCarrier],
                               parent2_carrier: Optional[GeneticCarrier]) -> Optional[GeneticCarrier]:
        """Inherit a single disease from parents."""
        # Get copies from each parent
        parent1_copies = parent1_carrier.copies if parent1_carrier else 0
        parent2_copies = parent2_carrier.copies if parent2_carrier else 0
        
        # Inherit based on inheritance pattern
        if disease.inheritance_pattern == InheritancePattern.AUTOSOMAL_DOMINANT:
            # Need only one copy from either parent
            inherited_copies = 0
            if parent1_copies > 0 and random.random() < 0.5:
                inherited_copies += 1
            if parent2_copies > 0 and random.random() < 0.5:
                inherited_copies += 1
            inherited_copies = min(inherited_copies, 1)
            
        elif disease.inheritance_pattern == InheritancePattern.AUTOSOMAL_RECESSIVE:
            # Can inherit 0, 1, or 2 copies
            inherited_copies = 0
            if parent1_copies > 0 and random.random() < 0.5:
                inherited_copies += 1
            if parent2_copies > 0 and random.random() < 0.5:
                inherited_copies += 1
                
        else:  # Other inheritance patterns simplified
            total_parent_copies = parent1_copies + parent2_copies
            inherited_copies = 1 if total_parent_copies > 0 and random.random() < 0.5 else 0
        
        if inherited_copies == 0:
            return None
        
        # Check expression
        expressed = self._check_disease_expression(disease, inherited_copies)
        
        # Determine onset age if expressed
        age_of_onset = None
        if expressed:
            min_onset, max_onset = disease.age_of_onset
            age_of_onset = random.randint(min_onset, max_onset)
        
        # Inherit progression rate (average of parents with some variance)
        parent1_rate = parent1_carrier.progression_rate if parent1_carrier else 1.0
        parent2_rate = parent2_carrier.progression_rate if parent2_carrier else 1.0
        avg_rate = (parent1_rate + parent2_rate) / 2
        progression_rate = max(0.1, avg_rate + random.uniform(-0.3, 0.3))
        
        return GeneticCarrier(
            disease_id=disease.id,
            copies=inherited_copies,
            expressed=expressed,
            age_of_onset=age_of_onset,
            severity=None,
            progression_rate=progression_rate,
            treatment_status=False
        )
    
    def process_daily_disease_effects(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process daily effects of genetic diseases on agents."""
        disease_events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            agent_genetics = self.agent_genetics.get(agent.id, {})
            
            for disease_id, carrier_info in agent_genetics.items():
                if not carrier_info.expressed:
                    # Check if disease should manifest
                    if (carrier_info.age_of_onset and 
                        agent.age >= carrier_info.age_of_onset and 
                        not carrier_info.expressed):
                        
                        carrier_info.expressed = True
                        carrier_info.severity = self._determine_initial_severity(self.diseases[disease_id])
                        
                        disease_events.append({
                            "type": "disease_onset",
                            "agent": agent.name,
                            "disease": self.diseases[disease_id].name,
                            "age": agent.age,
                            "severity": carrier_info.severity.value,
                            "day": current_day
                        })
                        
                        # Add memory of disease onset
                        agent.memory.store_memory(
                            f"Developed {self.diseases[disease_id].name} at age {agent.age}",
                            importance=0.8,
                            memory_type="health"
                        )
                
                # Apply disease effects if active
                if carrier_info.expressed:
                    disease_effect = self._apply_disease_effects(agent, disease_id, carrier_info, current_day)
                    if disease_effect:
                        disease_events.append(disease_effect)
        
        return disease_events
    
    def _determine_initial_severity(self, disease: GeneticDisease) -> DiseaseSeverity:
        """Determine initial severity when disease manifests."""
        # Usually starts at disease's base severity or lower
        if disease.severity == DiseaseSeverity.CRITICAL:
            return random.choices([DiseaseSeverity.SEVERE, DiseaseSeverity.CRITICAL],
                                weights=[0.7, 0.3])[0]
        elif disease.severity == DiseaseSeverity.SEVERE:
            return random.choices([DiseaseSeverity.MODERATE, DiseaseSeverity.SEVERE],
                                weights=[0.6, 0.4])[0]
        elif disease.severity == DiseaseSeverity.MODERATE:
            return random.choices([DiseaseSeverity.MILD, DiseaseSeverity.MODERATE],
                                weights=[0.7, 0.3])[0]
        else:
            return DiseaseSeverity.MILD
    
    def _apply_disease_effects(self, agent: Any, disease_id: str, 
                              carrier_info: GeneticCarrier, current_day: int) -> Optional[Dict[str, Any]]:
        """Apply daily effects of an active genetic disease."""
        disease = self.diseases[disease_id]
        
        # Calculate severity multiplier
        severity_multipliers = {
            DiseaseSeverity.MILD: 0.5,
            DiseaseSeverity.MODERATE: 1.0,
            DiseaseSeverity.SEVERE: 1.5,
            DiseaseSeverity.CRITICAL: 2.0
        }
        severity_mult = severity_multipliers[carrier_info.severity]
        
        # Calculate treatment modifier
        treatment_modifier = 1.0
        if carrier_info.treatment_status and disease.treatment_available:
            treatment_modifier = 1.0 - disease.treatment_effectiveness
        
        # Apply health impact
        health_impact = disease.health_impact * severity_mult * treatment_modifier * carrier_info.progression_rate
        agent.health = max(0.0, agent.health - health_impact)
        
        # Apply energy impact
        energy_impact = disease.energy_impact * severity_mult * treatment_modifier * carrier_info.progression_rate
        agent.energy = max(0.0, agent.energy - energy_impact)
        
        # Check for disease progression
        progression_chance = 0.001 * carrier_info.progression_rate  # Very slow progression
        if random.random() < progression_chance:
            if carrier_info.severity != DiseaseSeverity.CRITICAL:
                new_severity = self._progress_severity(carrier_info.severity)
                if new_severity != carrier_info.severity:
                    carrier_info.severity = new_severity
                    return {
                        "type": "disease_progression",
                        "agent": agent.name,
                        "disease": disease.name,
                        "new_severity": new_severity.value,
                        "day": current_day
                    }
        
        return None
    
    def _progress_severity(self, current_severity: DiseaseSeverity) -> DiseaseSeverity:
        """Progress disease to next severity level."""
        progression_map = {
            DiseaseSeverity.MILD: DiseaseSeverity.MODERATE,
            DiseaseSeverity.MODERATE: DiseaseSeverity.SEVERE,
            DiseaseSeverity.SEVERE: DiseaseSeverity.CRITICAL,
            DiseaseSeverity.CRITICAL: DiseaseSeverity.CRITICAL  # Cannot progress further
        }
        return progression_map[current_severity]
    
    def check_reproduction_compatibility(self, agent1: Any, agent2: Any) -> Tuple[bool, float, List[str]]:
        """Check genetic compatibility for reproduction."""
        compatibility = True
        risk_factor = 0.0
        warnings = []
        
        agent1_genetics = self.agent_genetics.get(agent1.id, {})
        agent2_genetics = self.agent_genetics.get(agent2.id, {})
        
        # Check for shared recessive diseases
        shared_diseases = set(agent1_genetics.keys()) & set(agent2_genetics.keys())
        
        for disease_id in shared_diseases:
            disease = self.diseases[disease_id]
            
            if disease.inheritance_pattern == InheritancePattern.AUTOSOMAL_RECESSIVE:
                # High risk if both are carriers
                risk_factor += 0.25  # 25% chance for each shared recessive
                warnings.append(f"Both carriers of {disease.name}")
            elif disease.inheritance_pattern == InheritancePattern.AUTOSOMAL_DOMINANT:
                # 50% chance of inheritance
                risk_factor += 0.5
                warnings.append(f"High chance of inheriting {disease.name}")
        
        # Calculate overall reproduction impact
        total_reproduction_impact = 0.0
        for carrier_info in agent1_genetics.values():
            if carrier_info.expressed:
                disease = self.diseases[carrier_info.disease_id]
                total_reproduction_impact += disease.reproduction_impact
        
        for carrier_info in agent2_genetics.values():
            if carrier_info.expressed:
                disease = self.diseases[carrier_info.disease_id]
                total_reproduction_impact += disease.reproduction_impact
        
        # High genetic disease burden reduces compatibility
        if total_reproduction_impact > 0.5:
            compatibility = False
            warnings.append("High genetic disease burden may affect reproduction")
        
        return compatibility, risk_factor, warnings
    
    def get_agent_health_summary(self, agent: Any) -> Dict[str, Any]:
        """Get comprehensive health summary including genetic diseases."""
        agent_genetics = self.agent_genetics.get(agent.id, {})
        
        active_diseases = []
        carrier_diseases = []
        health_impacts = {"total_health_impact": 0.0, "total_energy_impact": 0.0}
        
        for disease_id, carrier_info in agent_genetics.items():
            disease = self.diseases[disease_id]
            
            if carrier_info.expressed:
                active_diseases.append({
                    "name": disease.name,
                    "type": disease.disease_type.value,
                    "severity": carrier_info.severity.value,
                    "symptoms": disease.symptoms,
                    "treated": carrier_info.treatment_status
                })
                
                # Calculate current impacts
                severity_mult = {"mild": 0.5, "moderate": 1.0, "severe": 1.5, "critical": 2.0}[carrier_info.severity.value]
                treatment_mult = 1.0 - (disease.treatment_effectiveness if carrier_info.treatment_status else 0.0)
                
                health_impacts["total_health_impact"] += disease.health_impact * severity_mult * treatment_mult
                health_impacts["total_energy_impact"] += disease.energy_impact * severity_mult * treatment_mult
                
            else:
                carrier_diseases.append({
                    "name": disease.name,
                    "carrier_status": f"{carrier_info.copies} copies",
                    "onset_age": carrier_info.age_of_onset
                })
        
        return {
            "active_diseases": active_diseases,
            "carrier_diseases": carrier_diseases,
            "health_impacts": health_impacts,
            "genetic_risk_factors": len(agent_genetics),
            "treatment_needed": len([d for d in active_diseases if not d["treated"]])
        }
    
    def get_population_genetics_summary(self) -> Dict[str, Any]:
        """Get population-wide genetic health summary."""
        total_agents = len(self.agent_genetics)
        if total_agents == 0:
            return {"status": "no_data"}
        
        disease_prevalence = {}
        active_cases = {}
        carriers = {}
        
        for agent_id, genetics in self.agent_genetics.items():
            for disease_id, carrier_info in genetics.items():
                disease_name = self.diseases[disease_id].name
                
                # Count carriers
                carriers[disease_name] = carriers.get(disease_name, 0) + 1
                
                # Count active cases
                if carrier_info.expressed:
                    active_cases[disease_name] = active_cases.get(disease_name, 0) + 1
        
        # Calculate prevalence rates
        for disease_name, count in carriers.items():
            disease_prevalence[disease_name] = {
                "carrier_rate": count / total_agents,
                "active_rate": active_cases.get(disease_name, 0) / total_agents,
                "carriers": count,
                "active_cases": active_cases.get(disease_name, 0)
            }
        
        return {
            "total_population": total_agents,
            "diseases_tracked": len(self.diseases),
            "disease_prevalence": disease_prevalence,
            "population_health_trend": self._assess_population_health_trend(),
            "genetic_diversity": self._calculate_genetic_diversity()
        }
    
    def _assess_population_health_trend(self) -> str:
        """Assess overall population genetic health trend."""
        total_active = sum(
            len([c for c in genetics.values() if c.expressed])
            for genetics in self.agent_genetics.values()
        )
        total_possible = len(self.agent_genetics) * len(self.diseases)
        
        if total_possible == 0:
            return "insufficient_data"
        
        disease_rate = total_active / total_possible
        
        if disease_rate < 0.01:
            return "excellent"
        elif disease_rate < 0.05:
            return "good"
        elif disease_rate < 0.1:
            return "concerning"
        else:
            return "poor"
    
    def _calculate_genetic_diversity(self) -> float:
        """Calculate genetic diversity score."""
        if not self.agent_genetics:
            return 0.0
        
        # Count unique genetic profiles
        unique_profiles = set()
        for genetics in self.agent_genetics.values():
            profile = tuple(sorted([
                (disease_id, carrier.copies, carrier.expressed)
                for disease_id, carrier in genetics.items()
            ]))
            unique_profiles.add(profile)
        
        # Diversity = unique profiles / total agents
        return len(unique_profiles) / len(self.agent_genetics) 