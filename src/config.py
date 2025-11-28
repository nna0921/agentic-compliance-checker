import os

POLICY_RULES = [
    {
        "id": "R01",
        "category": "Governing Law",
        "description": "The agreement must be governed by the laws of the State of New York. (CUAD Cat 8)",
        "search_query": "governing law jurisdiction New York"
    },
    {
        "id": "R02",
        "category": "Termination for Convenience",
        "description": "We require the right to terminate the contract without cause (for convenience). (CUAD Cat 16)",
        "search_query": "terminate for convenience without cause termination notice"
    },
    {
        "id": "R03",
        "category": "Change of Control",
        "description": "We must have the right to terminate if the counterparty undergoes a Change of Control (e.g., merger/acquisition). (CUAD Cat 18)",
        "search_query": "change of control merger acquisition terminate"
    },
    {
        "id": "R04",
        "category": "Anti-Assignment",
        "description": "The counterparty cannot assign this contract to a third party without our prior written consent. (CUAD Cat 19)",
        "search_query": "assignment transfer rights consent not unreasonably withheld"
    },
    {
        "id": "R05",
        "category": "Non-Compete",
        "description": "The contract must NOT contain any non-compete clauses that restrict our business operations. (CUAD Cat 10)",
        "search_query": "non-compete restriction competition business sector"
    },
    {
        "id": "R06",
        "category": "Exclusivity",
        "description": "We do not agree to any exclusivity or 'exclusive dealing' commitments. (CUAD Cat 11)",
        "search_query": "exclusive dealing exclusivity sole provider"
    },
    {
        "id": "R07",
        "category": "No-Solicit of Employees",
        "description": "We do not accept restrictions on soliciting or hiring the counterparty's employees. (CUAD Cat 14)",
        "search_query": "non-solicitation solicit employees hire personnel"
    },
    {
        "id": "R08",
        "category": "Most Favored Nation",
        "description": "We require a 'Most Favored Nation' clause ensuring we get the best pricing available. (CUAD Cat 9)",
        "search_query": "most favored nation MFN best price lower price"
    },
    {
        "id": "R09",
        "category": "IP Ownership Assignment",
        "description": "Intellectual Property created during this engagement must be owned by US (the Client). (CUAD Cat 24)",
        "search_query": "intellectual property ownership assignment work made for hire"
    },
    {
        "id": "R10",
        "category": "Cap on Liability",
        "description": "Our liability must be capped at the total fees paid under the agreement. (CUAD Cat 36)",
        "search_query": "limitation of liability cap aggregate liability fees paid"
    },
    {
        "id": "R11",
        "category": "Uncapped Liability",
        "description": "We cannot accept uncapped liability for general breaches. (CUAD Cat 35)",
        "search_query": "uncapped liability unlimited liability indemnity"
    },
    {
        "id": "R12",
        "category": "Liquidated Damages",
        "description": "The contract should NOT contain liquidated damages (penalty fees) for breach. (CUAD Cat 37)",
        "search_query": "liquidated damages penalty fee breach"
    },

    # --- GROUP 4: OPERATIONAL & MISC ---
    {
        "id": "R13",
        "category": "Insurance",
        "description": "The counterparty is required to maintain professional liability or general liability insurance. (CUAD Cat 39)",
        "search_query": "insurance policy coverage maintain liability insurance"
    },
    {
        "id": "R14",
        "category": "Audit Rights",
        "description": "We must have the right to audit the counterparty's books and records. (CUAD Cat 34)",
        "search_query": "audit rights books records inspection examine"
    },
    {
        "id": "R15",
        "category": "Non-Disparagement",
        "description": "The agreement must include a mutual non-disparagement clause. (CUAD Cat 15)",
        "search_query": "non-disparagement disparage reputation negative statements"
    }
]

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
PDF_DIR = os.path.join(DATA_DIR, 'raw_pdfs')
DB_DIR = os.path.join(DATA_DIR, 'chroma_db')