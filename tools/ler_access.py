import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LERQueryEngine:
    """
    Basic query engine for accessing LER content
    Provides programmatic interface to EEP definitions, SOPs, and patterns
    """
    
    def __init__(self, ler_root_path: str = ".."):
        """
        Initialize the LER Query Engine
        
        Args:
            ler_root_path: Path to the root of the LER repository
        """
        self.ler_root = Path(ler_root_path)
        self.eep_definitions = {}
        self.sop_definitions = {}
        self.signature_patterns = {}
        self.schema = {}
        
        # Verify LER structure exists
        if not self.ler_root.exists():
            raise FileNotFoundError(f"LER root directory not found: {ler_root_path}")
        
        # Load all content
        self._load_schema()
        self._load_eep_definitions()
        self._load_sop_definitions()
        self._load_signature_patterns()
        
        logger.info(f"LER Query Engine initialized with {len(self.eep_definitions)} EEPs, "
                   f"{len(self.sop_definitions)} SOPs")

    def _load_yaml_file(self, file_path: Path) -> Optional[Dict]:
        """Load and parse a YAML file safely"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                logger.warning(f"File not found: {file_path}")
                return None
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return None

    def _load_schema(self):
        """Load the core schema definitions"""
        schema_path = self.ler_root / "schemas" / "core_schema.yaml"
        schema_data = self._load_yaml_file(schema_path)
        if schema_data:
            self.schema = schema_data
            logger.info("Core schema loaded successfully")

    def _load_eep_definitions(self):
        """Load all EEP definition files"""
        eep_dir = self.ler_root / "eep_definitions"
        if not eep_dir.exists():
            logger.warning(f"EEP definitions directory not found: {eep_dir}")
            return
        
        for eep_file in eep_dir.glob("*.yaml"):
            eep_data = self._load_yaml_file(eep_file)
            if eep_data and 'eep_id' in eep_data:
                self.eep_definitions[eep_data['eep_id']] = eep_data
                logger.debug(f"Loaded EEP: {eep_data['eep_id']}")

    def _load_sop_definitions(self):
        """Load all SOP definition files recursively"""
        sop_dir = self.ler_root / "sops"
        if not sop_dir.exists():
            logger.warning(f"SOPs directory not found: {sop_dir}")
            return
        
        for sop_file in sop_dir.rglob("*.yaml"):
            sop_data = self._load_yaml_file(sop_file)
            if sop_data and 'sop_id' in sop_data:
                self.sop_definitions[sop_data['sop_id']] = sop_data
                logger.debug(f"Loaded SOP: {sop_data['sop_id']}")

    def _load_signature_patterns(self):
        """Load signature pattern definitions"""
        patterns_dir = self.ler_root / "signature_patterns"
        if not patterns_dir.exists():
            logger.warning(f"Signature patterns directory not found: {patterns_dir}")
            return
        
        for pattern_file in patterns_dir.glob("*.yaml"):
            pattern_data = self._load_yaml_file(pattern_file)
            if pattern_data:
                # Signature patterns might be stored differently
                pattern_name = pattern_file.stem
                self.signature_patterns[pattern_name] = pattern_data

    # Core Query Methods
    
    def get_eep_definition(self, eep_id: str) -> Optional[Dict]:
        """
        Retrieve complete EEP definition by ID
        
        Args:
            eep_id: EEP identifier (e.g., 'EEP_DISTRIBUTED_INTELLIGENCE')
            
        Returns:
            Complete EEP definition dict or None if not found
        """
        return self.eep_definitions.get(eep_id)

    def get_sop_definition(self, sop_id: str) -> Optional[Dict]:
        """
        Retrieve complete SOP definition by ID
        
        Args:
            sop_id: SOP identifier (e.g., 'SOP_BASIC_EEP_FINGERPRINTING')
            
        Returns:
            Complete SOP definition dict or None if not found
        """
        return self.sop_definitions.get(sop_id)

    def get_sop_step_details(self, sop_id: str, step_id: str) -> Optional[Dict]:
        """
        Retrieve specific step details from a SOP
        
        Args:
            sop_id: SOP identifier
            step_id: Step identifier within the SOP
            
        Returns:
            Step definition dict or None if not found
        """
        sop = self.get_sop_definition(sop_id)
        if not sop or 'steps' not in sop:
            return None
        
        for step in sop['steps']:
            if step.get('step_id') == step_id:
                return step
        
        return None

    def get_eep_signature_patterns(self, eep_id: str) -> List[Dict]:
        """
        Get signature patterns for a specific EEP
        
        Args:
            eep_id: EEP identifier
            
        Returns:
            List of signature pattern definitions
        """
        eep = self.get_eep_definition(eep_id)
        if eep and 'signature_patterns' in eep:
            return eep['signature_patterns']
        return []

    def list_available_eeps(self) -> List[str]:
        """Return list of all available EEP IDs"""
        return list(self.eep_definitions.keys())

    def list_available_sops(self) -> List[str]:
        """Return list of all available SOP IDs"""
        return list(self.sop_definitions.keys())

    def get_eeps_by_category(self, category: str) -> List[Dict]:
        """
        Get all EEPs in a specific category
        
        Args:
            category: EEP category name
            
        Returns:
            List of EEP definitions in the category
        """
        return [eep for eep in self.eep_definitions.values() 
                if eep.get('category') == category]

    def find_sops_for_eep(self, eep_id: str) -> List[Dict]:
        """
        Find SOPs that can analyze a specific EEP
        
        Args:
            eep_id: EEP identifier
            
        Returns:
            List of SOP definitions that target this EEP
        """
        matching_sops = []
        for sop in self.sop_definitions.values():
            target_eeps = sop.get('target_eeps', [])
            if eep_id in target_eeps:
                matching_sops.append(sop)
        return matching_sops

    # Utility Methods for Filament Integration
    
    def get_stub_implementation(self, sop_id: str, step_id: str) -> Optional[str]:
        """
        Get the stub implementation code for a specific SOP step
        
        Args:
            sop_id: SOP identifier
            step_id: Step identifier
            
        Returns:
            Stub implementation code string or None
        """
        step = self.get_sop_step_details(sop_id, step_id)
        if step:
            return step.get('stub_implementation')
        return None

    def validate_eep_definition(self, eep_id: str) -> Dict[str, Any]:
        """
        Validate an EEP definition against the schema
        
        Args:
            eep_id: EEP identifier to validate
            
        Returns:
            Validation result dict with status and any errors
        """
        eep = self.get_eep_definition(eep_id)
        if not eep:
            return {"valid": False, "error": f"EEP {eep_id} not found"}
        
        # Basic validation - check required fields
        required_fields = ['eep_id', 'name', 'universal_function', 'category']
        missing_fields = [field for field in required_fields if field not in eep]
        
        if missing_fields:
            return {"valid": False, "error": f"Missing required fields: {missing_fields}"}
        
        return {"valid": True, "eep": eep}

    def search_eeps_by_function(self, search_term: str) -> List[Dict]:
        """
        Search EEPs by universal function description
        
        Args:
            search_term: Term to search for in function descriptions
            
        Returns:
            List of matching EEP definitions
        """
        matches = []
        search_lower = search_term.lower()
        
        for eep in self.eep_definitions.values():
            universal_function = eep.get('universal_function', '').lower()
            if search_lower in universal_function:
                matches.append(eep)
        
        return matches

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get overall LER system information
        
        Returns:
            Dict with system statistics and health info
        """
        return {
            "ler_root": str(self.ler_root),
            "total_eeps": len(self.eep_definitions),
            "total_sops": len(self.sop_definitions),
            "total_patterns": len(self.signature_patterns),
            "schema_loaded": bool(self.schema),
            "available_eeps": list(self.eep_definitions.keys()),
            "available_sops": list(self.sop_definitions.keys())
        }


# Example usage and testing functions
def example_usage():
    """Demonstrate basic LER Query Engine functionality"""
    try:
        # Initialize the engine
        ler = LERQueryEngine("./eep-ler")
        
        # Get system info
        print("=== LER System Info ===")
        info = ler.get_system_info()
        for key, value in info.items():
            print(f"{key}: {value}")
        
        print("\n=== Available EEPs ===")
        for eep_id in ler.list_available_eeps():
            eep = ler.get_eep_definition(eep_id)
            print(f"- {eep_id}: {eep.get('name', 'Unknown')}")
        
        print("\n=== Available SOPs ===")
        for sop_id in ler.list_available_sops():
            sop = ler.get_sop_definition(sop_id)
            print(f"- {sop_id}: {sop.get('name', 'Unknown')}")
        
        # Test specific queries
        print("\n=== EEP Details Example ===")
        eep = ler.get_eep_definition("EEP_DISTRIBUTED_INTELLIGENCE")
        if eep:
            print(f"Name: {eep['name']}")
            print(f"Category: {eep['category']}")
            print(f"Function: {eep['universal_function'][:100]}...")
        
        print("\n=== SOP Step Example ===")
        step = ler.get_sop_step_details("SOP_BASIC_EEP_FINGERPRINTING", "STEP_2_SIGNATURE_SCANNING")
        if step:
            print(f"Step: {step['step_name']}")
            print(f"Purpose: {step['purpose']}")
        
    except Exception as e:
        print(f"Example failed: {e}")


if __name__ == "__main__":
    example_usage()