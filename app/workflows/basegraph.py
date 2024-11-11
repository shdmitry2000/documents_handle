from langchain import Graph, Node
from langchain.document_loaders import TextLoader
from langchain.prompts import PromptTemplate
from app.modules import layoutlmv3, donut, gemini, metadata

# Define prompt template for extraction
extract_prompt = PromptTemplate(input_variables=["file_url", "fields"], 
                                template="Extract the following fields: {fields} from the document located at {file_url}")

# Define the function to check file metadata and LLM verification
def metadata_identification(file_url):
    return metadata.identify_metadata(file_url)

# LayoutLMv3 Extraction Node
def layoutlmv3_extraction(file_url, fields):
    return layoutlmv3.extract_with_layoutlmv3(file_url, fields)

# Donut Extraction Node
def donut_extraction(file_url, fields):
    return donut.extract_with_donut(file_url, fields)

# Gemini LLM Extraction Node
def gemini_extraction(file_url, fields):
    return gemini.extract_with_gemini(file_url, fields)

# Define the LLM post-processing node
def llm_post_processing(extracted_data):
    # This could call another LLM to validate or improve the extraction
    return extracted_data  # Stub for now

# Build the LangGraph
def build_graph(file_url, fields):
    # Initialize graph
    graph = Graph()

    # Node 1: Initial file identification with LLM and metadata
    node_metadata = Node(func=metadata_identification, input_args=["file_url"])
    
    # Node 2: LayoutLMv3 Extraction
    node_layoutlmv3 = Node(func=layoutlmv3_extraction, input_args=["file_url", "fields"])

    # Node 3: Donut Extraction
    node_donut = Node(func=donut_extraction, input_args=["file_url", "fields"])

    # Node 4: Gemini LLM Extraction
    node_gemini = Node(func=gemini_extraction, input_args=["file_url", "fields"])

    # Node 5: LLM Post-Processing (refining or validating extracted data)
    node_post_process_layout = Node(func=llm_post_processing, input_args=["layoutlmv3_data"])
    node_post_process_donut = Node(func=llm_post_processing, input_args=["donut_data"])
    node_post_process_gemini = Node(func=llm_post_processing, input_args=["gemini_data"])

    # Add nodes to the graph
    graph.add_nodes([node_metadata, node_layoutlmv3, node_donut, node_gemini, 
                     node_post_process_layout, node_post_process_donut, node_post_process_gemini])

    # Link nodes together
    graph.add_edge(node_metadata, node_layoutlmv3)
    graph.add_edge(node_metadata, node_donut)
    graph.add_edge(node_metadata, node_gemini)

    graph.add_edge(node_layoutlmv3, node_post_process_layout)
    graph.add_edge(node_donut, node_post_process_donut)
    graph.add_edge(node_gemini, node_post_process_gemini)

    # Run the graph and return the output
    graph.run({"file_url": file_url, "fields": fields})
