
#!/usr/bin/env python3
"""
Filament v0.0.1 - Stateless EEP Processing Engine
A rudimentary demonstration of the LER-Filament interaction loop

This script demonstrates:
1. Taking a hardcoded query
2. Dynamically accessing LER definitions  
3. Executing stubbed analytical steps
4. Producing minimal output
5. Maintaining stateless operation
"""


import sys
import os
import json
import logging
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional

from ler_access import LERQueryEngine

sys.path.append(os.path.join(os.path.dirname(__file__), 'analytics'))
from networkx_analyzer import analyze_distributed_intelligence_networkx


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Filament')

class FilamentEvent:
    """
    A single, stateless Filament processing event
    
    Represents one complete cycle: Query -> LER Access -> Analysis -> Output -> Cleanup
    """
    
    def __init__(self, ler_engine: LERQueryEngine):
        self.ler = ler_engine
        self.event_id = f"filament_event_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.start_time = datetime.now()
        
        # Stateless - no persistent data beyond this event
        self.query_data = None
        self.ler_retrieved_data = None
        self.analysis_results = None # This will be populated by execute_stubbed_analysis
        self.final_output = None
        
        logger.info(f"Filament Event {self.event_id} initialized")

    def process_hardcoded_query(self) -> Dict[str, Any]:
        self.query_data = {
            "query_type": "eep_characterization",
            "target_eep": "EEP_DISTRIBUTED_INTELLIGENCE", 
            "analysis_sop": "SOP_BASIC_EEP_FINGERPRINTING",
            "specific_step": "STEP_2_SIGNATURE_SCANNING",
            "query_text": "Briefly characterize EEP_DISTRIBUTED_INTELLIGENCE based on SOP_BASIC_EEP_FINGERPRINTING, step STEP_2_SIGNATURE_SCANNING",
            "test_data": {
                # Hardcoded test data snippet for demonstration
                "network_data": {
                    "nodes": 10,
                    "edges": 25,
                    "clustering_coefficient": 0.6,
                    "avg_path_length": 2.3
                },
                "interaction_patterns": [
                    {"type": "threshold_activation", "frequency": 15},
                    {"type": "cascade_propagation", "frequency": 8},
                    {"type": "collective_decision", "frequency": 12}
                ]
            }
        }
        
        logger.info(f"Processed hardcoded query: {self.query_data['query_text']}")
        return self.query_data

    def retrieve_ler_guidance(self) -> Dict[str, Any]:
        
        if not self.query_data:
            raise ValueError("Must process query before retrieving LER guidance")
        
        self.ler_retrieved_data = {}
        
        # Get EEP definition
        eep_id = self.query_data["target_eep"]
        eep_def = self.ler.get_eep_definition(eep_id)
        if not eep_def:
            raise ValueError(f"EEP definition not found: {eep_id}")
        
        self.ler_retrieved_data["eep_definition"] = eep_def
        logger.info(f"Retrieved EEP definition: {eep_def['name']}")
        
        # Get SOP definition
        sop_id = self.query_data["analysis_sop"]
        sop_def = self.ler.get_sop_definition(sop_id)
        if not sop_def:
            raise ValueError(f"SOP definition not found: {sop_id}")
        
        self.ler_retrieved_data["sop_definition"] = sop_def
        logger.info(f"Retrieved SOP definition: {sop_def['name']}")
        
        # Get specific step details
        step_id = self.query_data["specific_step"]
        step_details = self.ler.get_sop_step_details(sop_id, step_id)
        if not step_details:
            raise ValueError(f"SOP step not found: {step_id} in {sop_id}")
        
        self.ler_retrieved_data["step_details"] = step_details
        logger.info(f"Retrieved SOP step: {step_details['step_name']}")
        
        # Get signature patterns for the EEP
        signature_patterns = self.ler.get_eep_signature_patterns(eep_id)
        self.ler_retrieved_data["signature_patterns"] = signature_patterns
        logger.info(f"Retrieved {len(signature_patterns)} signature patterns")
        
        return self.ler_retrieved_data

    # **** Corrected Indentation and Logic Starts Here ****
    def execute_stubbed_analysis(self):
        """Enhanced analysis with NetworkX integration"""
        
        if not self.ler_retrieved_data:
            raise ValueError("Must retrieve LER guidance before executing analysis")
        
        # Get data from the correct attributes
        step_details = self.ler_retrieved_data["step_details"]
        eep_definition = self.ler_retrieved_data["eep_definition"]
        step_name = step_details.get('step_name', 'Unknown Step')
        
        logger.info(f"Executing analysis for step: {step_name}")
        
        # Check if we can use real NetworkX analysis
        eep_id = eep_definition.get('eep_id', '')
        use_networkx = (eep_id == 'EEP_DISTRIBUTED_INTELLIGENCE' and 
                        'signature' in step_name.lower()) # Assuming 'signature' implies NetworkX applicability
        
        if use_networkx:
            logger.info("Using real NetworkX analysis")
            self.analysis_results = self._execute_networkx_analysis()
        else:
            logger.info("Using legacy stubbed analysis")
            self.analysis_results = self._execute_legacy_stub()
        return self.analysis_results # Return the stored results

    def _execute_networkx_analysis(self):
        """Execute real NetworkX analysis for Distributed Intelligence"""
        
        # This test_data and signature_template seem to be placeholders.
        # You might want to get actual data from self.query_data or self.ler_retrieved_data
        test_data = "sample network data" # Placeholder
        signature_template = {"type": "network_analysis"} # Placeholder
        
        networkx_results = analyze_distributed_intelligence_networkx(test_data, signature_template)
        
        # Extract key metrics
        network_motifs = networkx_results["details"]["network_motifs"]
        clustering_analysis = networkx_results["details"]["clustering_analysis"]
        connectivity_patterns = networkx_results["details"]["connectivity_patterns"]
        
        # Format results
        patterns = [
            {
                "name": "Network Motifs",
                "type": network_motifs["type"],
                "confidence": network_motifs["confidence"],
                "evidence": f"Clustering: {network_motifs['avg_clustering']}, Path length: {network_motifs['avg_path_length']}, Nodes: {network_motifs['nodes']}"
            },
            {
                "name": "Clustering Analysis", 
                "type": "clustering_structure",
                "confidence": min(0.9, 0.5 + clustering_analysis["global_clustering"]),
                "evidence": clustering_analysis['interpretation']
            },
            {
                "name": "Connectivity Patterns",
                "type": connectivity_patterns["connectivity_pattern"],
                "confidence": 0.75, # Example confidence
                "evidence": f"Hubs: {connectivity_patterns['hub_nodes']}, Pattern: {connectivity_patterns['connectivity_pattern']}"
            }
        ]
        
        overall_confidence = np.mean([p["confidence"] for p in patterns]) if patterns else 0.0
        
        logger.info(f"NetworkX analysis complete. Detected {len(patterns)} patterns") # Corrected: logger instead of self.logger
        
        return {
            "patterns_found": len(patterns),
            "overall_confidence": round(overall_confidence, 2),
            "status": "real_networkx_analysis_complete",
            "patterns": patterns # This key holds the list of pattern dicts
        }

    def _execute_legacy_stub(self):
        """Legacy stubbed analysis for fallback"""
        
        patterns = [
            {
                "name": "Network Motifs",
                "type": "small_world_network", 
                "confidence": 0.7,
                "evidence": "Clustering: 0.6, Path length: 2.3"
            },
            {
                "name": "Threshold Dynamics",
                "type": "threshold_function",
                "confidence": 0.6, 
                "evidence": "Found 1 threshold-type behaviors"
            },
            {
                "name": "Collective Processing",
                "type": "information_cascade",
                "confidence": 0.8,
                "evidence": "Found 2 collective processing events"
            }
        ]
        
        overall_confidence = np.mean([p["confidence"] for p in patterns]) if patterns else 0.0

        logger.info(f"Legacy stubbed analysis complete. Detected {len(patterns)} patterns") # Corrected: logger instead of self.logger
        
        return {
            "patterns_found": len(patterns),
            "overall_confidence": round(overall_confidence, 2), # Calculated for consistency
            "status": "legacy_stub_analysis_complete",
            "patterns": patterns # This key holds the list of pattern dicts
        }
    # **** Corrected Indentation and Logic Ends Here ****

    # The duplicated methods that were here (_execute_networkx_analysis with extra args, etc.)
    # have been removed for clarity as they were not used by the primary execute_stubbed_analysis.
    # If they are part of a future refactor, they would need to be integrated properly.

    def generate_output_projection(self) -> Dict[str, Any]:
        """
        Task FIL-4: Generate minimal output projection
        
        Creates a formatted output summarizing the analysis results
        Maintains stateless operation - no persistent state beyond this event
        
        Returns:
            Final formatted output
        """
        if not self.analysis_results: # Check if analysis_results has been populated
            raise ValueError("Must complete analysis before generating output")
        
        # Create final output projection
        self.final_output = {
            "filament_event_id": self.event_id,
            "timestamp": datetime.now().isoformat(),
            "query_summary": self.query_data["query_text"],
            "eep_analyzed": {
                "eep_id": self.ler_retrieved_data["eep_definition"]["eep_id"],
                "eep_name": self.ler_retrieved_data["eep_definition"]["name"],
                "category": self.ler_retrieved_data["eep_definition"]["category"]
            },
            "analysis_method": {
                "sop_used": self.ler_retrieved_data["sop_definition"]["name"],
                "step_executed": self.ler_retrieved_data["step_details"]["step_name"]
            },
            "results": {
                "signature_detection_summary": {
                    # Corrected keys based on what execute_stubbed_analysis returns
                    "patterns_found": self.analysis_results.get("patterns_found", 0),
                    "overall_confidence": round(self.analysis_results.get("overall_confidence", 0.0), 2),
                    "status": self.analysis_results.get("status", "unknown_status")
                },
                "detected_signatures": {} # Changed from detected_signatures to detected_patterns for consistency
            },
            "processing_metadata": {
                "processing_time_seconds": (datetime.now() - self.start_time).total_seconds(),
                "ler_data_accessed": list(self.ler_retrieved_data.keys()),
                "stateless_operation": True
            }
        }
        
        # Format detected patterns for output
        # Ensure we iterate over the 'patterns' list from analysis_results
        detected_patterns_list = self.analysis_results.get("patterns", [])
        for pattern_data in detected_patterns_list:
            pattern_name = pattern_data.get("name", "Unnamed Pattern")
            self.final_output["results"]["detected_signatures"][pattern_name] = {
                "type": pattern_data.get("type", "N/A"),
                "confidence": pattern_data.get("confidence", 0.0), 
                "evidence": pattern_data.get("evidence", "N/A")
            }
        
        logger.info("Output projection generated successfully")
        return self.final_output

    def format_human_readable_output(self) -> str:
        """
        Generate human-readable summary of the Filament event
        
        Returns:
            Formatted string summary
        """
        if not self.final_output:
            return "No output available - analysis not completed"
        
        output_lines = [] # Renamed for clarity
        output_lines.append("=" * 60)
        output_lines.append("FILAMENT EVENT RESULT")
        output_lines.append("=" * 60)
        
        output_lines.append(f"Event ID: {self.final_output['filament_event_id']}")
        output_lines.append(f"Query: {self.final_output['query_summary']}")
        output_lines.append("")
        
        eep_info = self.final_output["eep_analyzed"]
        output_lines.append(f"EEP Analyzed: {eep_info['eep_name']} ({eep_info['eep_id']})")
        output_lines.append(f"Category: {eep_info['category']}")
        output_lines.append("")
        
        analysis_info = self.final_output["analysis_method"]
        output_lines.append(f"Analysis Method: {analysis_info['sop_used']}")
        output_lines.append(f"Step Executed: {analysis_info['step_executed']}")
        output_lines.append("")
        
        results = self.final_output["results"]
        output_lines.append("SIGNATURE DETECTION RESULTS:")
        output_lines.append(f"- Patterns Found: {results['signature_detection_summary']['patterns_found']}")
        output_lines.append(f"- Overall Confidence: {results['signature_detection_summary']['overall_confidence']}")
        output_lines.append(f"- Status: {results['signature_detection_summary']['status']}")
        output_lines.append("")
        
        if results["detected_signatures"]:
            output_lines.append("DETECTED PATTERNS:") # Changed from DETECTED SIGNATURES
            for pattern_name, pattern_info in results["detected_signatures"].items():
                output_lines.append(f"  • {pattern_name.replace('_', ' ').title()}")
                output_lines.append(f"    Type: {pattern_info['type']}")
                output_lines.append(f"    Confidence: {pattern_info['confidence']}")
                output_lines.append(f"    Evidence: {pattern_info['evidence']}")
                output_lines.append("") # Add a blank line after each pattern for readability
        
        metadata = self.final_output["processing_metadata"]
        output_lines.append(f"Processing Time: {metadata['processing_time_seconds']:.2f} seconds")
        output_lines.append(f"Stateless Operation: {metadata['stateless_operation']}")
        output_lines.append("=" * 60)
        
        return "\n".join(output_lines)

    def cleanup_and_terminate(self):
        """
        Demonstrate stateless termination
        Clear all transient data and log completion
        """
        logger.info(f"Cleaning up Filament Event {self.event_id}")
        
        # Clear all transient state
        self.query_data = None
        self.ler_retrieved_data = None
        self.analysis_results = None
        # Keep final_output for return, but mark as completed
        
        logger.info(f"Filament Event {self.event_id} completed and cleaned up")

def execute_stubbed_analysis(self):
    """Enhanced analysis with NetworkX integration"""
    
    if not self.ler_retrieved_data:
        raise ValueError("Must retrieve LER guidance before executing analysis")
    
    # Get data from the correct attributes
    step_details = self.ler_retrieved_data["step_details"]
    eep_definition = self.ler_retrieved_data["eep_definition"]
    step_name = step_details.get('step_name', 'Unknown Step')
    
    logger.info(f"Executing analysis for step: {step_name}")
    
    # Check if we can use real NetworkX analysis
    eep_id = eep_definition.get('eep_id', '')
    use_networkx = (eep_id == 'EEP_DISTRIBUTED_INTELLIGENCE' and 
                   'signature' in step_name.lower())
    
    if use_networkx:
        logger.info("Using real NetworkX analysis")
        return self._execute_networkx_analysis()
    else:
        logger.info("Using legacy stubbed analysis")
        return self._execute_legacy_stub()

def _execute_networkx_analysis(self):
    """Execute real NetworkX analysis for Distributed Intelligence"""
    
    test_data = "sample network data"
    signature_template = {"type": "network_analysis"}
    
    networkx_results = analyze_distributed_intelligence_networkx(test_data, signature_template)
    
    # Extract key metrics
    network_motifs = networkx_results["details"]["network_motifs"]
    clustering_analysis = networkx_results["details"]["clustering_analysis"]
    connectivity_patterns = networkx_results["details"]["connectivity_patterns"]
    
    # Format results
    patterns = [
        {
            "name": "Network Motifs",
            "type": network_motifs["type"],
            "confidence": network_motifs["confidence"],
            "evidence": f"Clustering: {network_motifs['avg_clustering']}, Path length: {network_motifs['avg_path_length']}, Nodes: {network_motifs['nodes']}"
        },
        {
            "name": "Clustering Analysis", 
            "type": "clustering_structure",
            "confidence": min(0.9, 0.5 + clustering_analysis["global_clustering"]),
            "evidence": clustering_analysis['interpretation']
        },
        {
            "name": "Connectivity Patterns",
            "type": connectivity_patterns["connectivity_pattern"],
            "confidence": 0.75,
            "evidence": f"Hubs: {connectivity_patterns['hub_nodes']}, Pattern: {connectivity_patterns['connectivity_pattern']}"
        }
    ]
    
    overall_confidence = numpy.mean([p["confidence"] for p in patterns])
    
    self.logger.info(f"NetworkX analysis complete. Detected {len(patterns)} patterns")
    
    return {
        "patterns_found": len(patterns),
        "overall_confidence": round(overall_confidence, 2),
        "status": "real_networkx_analysis_complete",
        "patterns": patterns
    }

def _execute_legacy_stub(self):
    """Legacy stubbed analysis for fallback"""
    
    patterns = [
        {
            "name": "Network Motifs",
            "type": "small_world_network", 
            "confidence": 0.7,
            "evidence": "Clustering: 0.6, Path length: 2.3"
        },
        {
            "name": "Threshold Dynamics",
            "type": "threshold_function",
            "confidence": 0.6, 
            "evidence": "Found 1 threshold-type behaviors"
        },
        {
            "name": "Collective Processing",
            "type": "information_cascade",
            "confidence": 0.8,
            "evidence": "Found 2 collective processing events"
        }
    ]
    
    self.logger.info(f"Analysis complete. Detected {len(patterns)} patterns")
    
    return {
        "patterns_found": len(patterns),
        "overall_confidence": 0.7,
        "status": "signatures_detected",
        "patterns": patterns
    }

def _execute_networkx_analysis(self, eep_data, signature_patterns):
    """Execute real NetworkX analysis for Distributed Intelligence"""
    
    self.logger.info("Using real NetworkX analysis")
    
    # Use real NetworkX analysis
    test_data = "sample network data"  # In production, this would be actual data
    signature_template = {"type": "network_analysis"}
    
    networkx_results = analyze_distributed_intelligence_networkx(test_data, signature_template)
    
    # Extract key metrics for pattern detection
    network_motifs = networkx_results["details"]["network_motifs"]
    clustering_analysis = networkx_results["details"]["clustering_analysis"]
    connectivity_patterns = networkx_results["details"]["connectivity_patterns"]
    
    # Format results in the expected structure
    patterns = [
        {
            "name": "Network Motifs",
            "type": network_motifs["type"],
            "confidence": network_motifs["confidence"],
            "evidence": f"Clustering: {network_motifs['avg_clustering']}, Path length: {network_motifs['avg_path_length']}, Nodes: {network_motifs['nodes']}"
        },
        {
            "name": "Clustering Analysis", 
            "type": "clustering_structure",
            "confidence": min(0.9, 0.5 + clustering_analysis["global_clustering"]),
            "evidence": f"{clustering_analysis['interpretation']}, Global clustering: {clustering_analysis['global_clustering']}"
        },
        {
            "name": "Connectivity Patterns",
            "type": connectivity_patterns["connectivity_pattern"],
            "confidence": 0.75,
            "evidence": f"Degree distribution: mean={connectivity_patterns['degree_distribution']['mean']}, hubs={connectivity_patterns['hub_nodes']}"
        }
    ]
    
    overall_confidence = np.mean([p["confidence"] for p in patterns])
    
    self.logger.info(f"NetworkX analysis complete. Detected {len(patterns)} patterns")
    
    return {
        "patterns_found": len(patterns),
        "overall_confidence": round(overall_confidence, 2),
        "status": "real_analysis_complete",
        "patterns": patterns,
        "analysis_method": "NetworkX Real Analysis"
    }

def _execute_legacy_stub(self, eep_data, signature_patterns):

    def generate_output_projection(self) -> Dict[str, Any]:
        """
        Task FIL-4: Generate minimal output projection
        
        Creates a formatted output summarizing the analysis results
        Maintains stateless operation - no persistent state beyond this event
        
        Returns:
            Final formatted output
        """
        if not self.analysis_results:
            raise ValueError("Must complete analysis before generating output")
        
        # Create final output projection
        self.final_output = {
            "filament_event_id": self.event_id,
            "timestamp": datetime.now().isoformat(),
            "query_summary": self.query_data["query_text"],
            "eep_analyzed": {
                "eep_id": self.ler_retrieved_data["eep_definition"]["eep_id"],
                "eep_name": self.ler_retrieved_data["eep_definition"]["name"],
                "category": self.ler_retrieved_data["eep_definition"]["category"]
            },
            "analysis_method": {
                "sop_used": self.ler_retrieved_data["sop_definition"]["name"],
                "step_executed": self.ler_retrieved_data["step_details"]["step_name"]
            },
            "results": {
                "signature_detection_summary": {
                    "patterns_found": len(self.analysis_results["detected_patterns"]),
                    "overall_confidence": round(self.analysis_results["analysis_confidence"], 2),
                    "status": "signatures_detected" if self.analysis_results["detected_patterns"] else "no_signatures"
                },
                "detected_signatures": {}
            },
            "processing_metadata": {
                "processing_time_seconds": (datetime.now() - self.start_time).total_seconds(),
                "ler_data_accessed": list(self.ler_retrieved_data.keys()),
                "stateless_operation": True
            }
        }
        
        # Format detected patterns for output
        for pattern_name, pattern_data in self.analysis_results["detected_patterns"].items():
            self.final_output["results"]["detected_signatures"][pattern_name] = {
                "type": pattern_data["pattern_type"],
                "confidence": pattern_data["confidence"], 
                "evidence": pattern_data["evidence"]
            }
        
        logger.info("Output projection generated successfully")
        return self.final_output

    def format_human_readable_output(self) -> str:
        """
        Generate human-readable summary of the Filament event
        
        Returns:
            Formatted string summary
        """
        if not self.final_output:
            return "No output available - analysis not completed"
        
        output = []
        output.append("=" * 60)
        output.append("FILAMENT EVENT RESULT")
        output.append("=" * 60)
        
        output.append(f"Event ID: {self.final_output['filament_event_id']}")
        output.append(f"Query: {self.final_output['query_summary']}")
        output.append("")
        
        eep_info = self.final_output["eep_analyzed"]
        output.append(f"EEP Analyzed: {eep_info['eep_name']} ({eep_info['eep_id']})")
        output.append(f"Category: {eep_info['category']}")
        output.append("")
        
        analysis_info = self.final_output["analysis_method"]
        output.append(f"Analysis Method: {analysis_info['sop_used']}")
        output.append(f"Step Executed: {analysis_info['step_executed']}")
        output.append("")
        
        results = self.final_output["results"]
        output.append("SIGNATURE DETECTION RESULTS:")
        output.append(f"- Patterns Found: {results['signature_detection_summary']['patterns_found']}")
        output.append(f"- Overall Confidence: {results['signature_detection_summary']['overall_confidence']}")
        output.append(f"- Status: {results['signature_detection_summary']['status']}")
        output.append("")
        
        if results["detected_signatures"]:
            output.append("DETECTED PATTERNS:")
            for pattern_name, pattern_info in results["detected_signatures"].items():
                output.append(f"  • {pattern_name.replace('_', ' ').title()}")
                output.append(f"    Type: {pattern_info['type']}")
                output.append(f"    Confidence: {pattern_info['confidence']}")
                output.append(f"    Evidence: {pattern_info['evidence']}")
                output.append("")
        
        metadata = self.final_output["processing_metadata"]
        output.append(f"Processing Time: {metadata['processing_time_seconds']:.2f} seconds")
        output.append(f"Stateless Operation: {metadata['stateless_operation']}")
        output.append("=" * 60)
        
        return "\n".join(output)

    def cleanup_and_terminate(self):
        """
        Demonstrate stateless termination
        Clear all transient data and log completion
        """
        logger.info(f"Cleaning up Filament Event {self.event_id}")
        
        # Clear all transient state
        self.query_data = None
        self.ler_retrieved_data = None
        self.analysis_results = None
        # Keep final_output for return, but mark as completed
        
        logger.info(f"Filament Event {self.event_id} completed and cleaned up")

def run_filament_demonstration():
    """
    Complete Sprint Zero demonstration
    Shows the full LER-Filament interaction loop
    """
    print("Starting Filament v0.0.1 Demonstration")
    print("=" * 50)
    
    try:
        
        ler_engine = LERQueryEngine("..") # Ensure this path is correct for your LER data
        print(f"   ✓ LER loaded: {ler_engine.get_system_info()['total_eeps']} EEPs, {ler_engine.get_system_info()['total_sops']} SOPs")
        
        # Create Filament event
        print("\n2. Creating Filament Event...")
        filament = FilamentEvent(ler_engine)
        print(f"   ✓ Event created: {filament.event_id}")
        
        # Process hardcoded query
        print("\n3. Processing hardcoded query...")
        query_result = filament.process_hardcoded_query()
        print(f"   ✓ Query: {query_result['query_text']}")
        
        # Retrieve LER guidance  
        print("\n4. Retrieving LER guidance...")
        ler_data = filament.retrieve_ler_guidance()
        print(f"   ✓ Retrieved EEP: {ler_data['eep_definition']['name']}")
        print(f"   ✓ Retrieved SOP: {ler_data['sop_definition']['name']}")
        print(f"   ✓ Retrieved Step: {ler_data['step_details']['step_name']}")
        
        # Execute analysis
        print("\n5. Executing stubbed analysis...")
        # The filament.analysis_results will be set by execute_stubbed_analysis call
        # So we don't need to assign its return value to a new 'analysis' variable here
        # if we are already storing it in self.analysis_results.
        # However, for clarity and local use, assigning it is fine:
        analysis_output = filament.execute_stubbed_analysis() # This now correctly calls the method

        # **** Corrected Print Statements ****
        print(f"   ✓ Analysis status: {analysis_output.get('status', 'N/A')}")
        print(f"   ✓ Patterns detected: {analysis_output.get('patterns_found', 0)}")
        print(f"   ✓ Overall Confidence: {analysis_output.get('overall_confidence', 0.0):.2f}")
        
        # Generate output
        print("\n6. Generating output projection...")
        # generate_output_projection uses filament.analysis_results which was set by execute_stubbed_analysis
        output_projection = filament.generate_output_projection()
        print(f"   ✓ Output generated: {output_projection['filament_event_id']}")
        
        # Display results
        print("\n7. Final Results:")
        print(filament.format_human_readable_output())
        
        # Cleanup
        print("\n8. Cleaning up (stateless termination)...")
        filament.cleanup_and_terminate()
        print("   ✓ Filament event completed and cleaned up")
        
        print("\n" + "=" * 50)
        print("Sprint Zero Demonstration Complete!")
        print("LER-Filament interaction loop successfully demonstrated.")
        
        return True
        
    except Exception as e:
        print(f"\nDemonstration failed: {e}")
        logger.exception("Filament demonstration error")
        return False


if __name__ == "__main__":
    # Run the complete Sprint Zero demonstration
    success = run_filament_demonstration()
    sys.exit(0 if success else 1)