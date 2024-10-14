import uuid  # For generating UUIDs for associations

from biolink_model.datamodel.pydanticmodel_v2 import *  # Replace * with any necessary data classes from the Biolink Model
from koza.cli_utils import get_koza_app

koza_app = get_koza_app("string_modular")

while (row := koza_app.get_row()) is not None:
    # Code to transform each row of data
    # For more information, see https://koza.monarchinitiative.org/Ingests/transform
    entity_a = Protein(
        id=f"{row['protein1'].split('.')[1]}",
        name=row["protein1"],
    )
    entity_b = Protein(
        id=f"{row['protein2'].split('.')[1]}",
        name=row["protein2"],
    )
    # make a list of evidence, e.g.
    # neighborhood fusion cooccurence coexpression experimental database textmining combined_score
    # and put it in has_attribute
    list_of_evidence = []
    for key in row.keys():
        list_of_evidence.append(f"{key}:{row[key]}")

    association = PairwiseMolecularInteraction(
        id=str(uuid.uuid1()),
        subject=row["protein1"],
        predicate="biolink:interacts_with",
        object=row["protein2"],
        subject_category="biolink:Protein",
        object_category="biolink:Protein",
        knowledge_level="not_provided",
        agent_type="not_provided",
        has_attribute=list_of_evidence
    )
    koza_app.write(entity_a, entity_b, association)
