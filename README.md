## Project Overview
Ariane is an interactive narrative engine with a web (Flask/JS) demo. The main data structure is a tree of story nodes, each with text, options (mapping words to child node IDs), and children. The story tree is persisted as JSON.

## Key Components

- `app.py`: Flask backend. Handles routes for serving the main page, fetching story nodes (`/continue?node_id=...`), expanding the story with LLM (`/expand`), and loading/saving the tree from `story/narrative_oriented_tree.json`.
- `story_tree.py`: Defines `Node` and `StoryTree` classes. Each node has an `id` (UUID), `text`, `options` (word→child id), and `children`. Use `to_dict`/`from_dict` for (de)serialization.
- `llm_utils.py`: Handles LLM calls (Mistral API) to generate new story text.
- `static/script.js`: Frontend logic. Loads nodes, displays clickable words, manages navigation history, and calls `/expand` if a word is not yet in the tree.
- `templates/index.html`: Main UI, centered layout, injects controls and story dynamically.
- `story/narrative_oriented_tree.json`: The canonical story tree, with each node containing `id`, `text`, `options`, and `children`.
- `scripts/tree_from_flat_dict.py`: Converts a flat dict to the nested tree structure, assigning UUIDs and building the `options` mapping.

## Data Flow

- On page load, JS fetches the root node (`start`) via `/continue?node_id=start`.
- Clicking a word triggers a lookup in the current node's `options`. If found, loads the child node by id. If not, calls `/expand` to generate and persist a new node.
- All navigation and expansion is reflected in the JSON tree, which is always the source of truth.

## Patterns & Conventions

- Node IDs are UUIDs (see `tree_from_flat_dict.py`), but you may use simpler unique keys if you update all references.
- The `options` field in each node is essential: it maps words in the text to the corresponding child node's id.
- All tree mutations (expansion) must update `story/narrative_oriented_tree.json` via the backend.
- Frontend and backend communicate exclusively via REST endpoints (`/continue`, `/expand`).

## Developer Workflows

- To rebuild the tree from a flat dict, run `scripts/tree_from_flat_dict.py`.
- To add new LLM-generated branches, interact with the UI or call `/expand` via POST.
- To debug navigation, use browser console logs (visited nodes, navigation history).
- To reset or edit the story, modify `story/narrative_oriented_tree.json` directly or regenerate it.

## Integration Points

- Mistral LLM API (see `llm_utils.py`), requires `MISTRAL_API_KEY` and `ARIANE_AGENT_ID` in environment.
- All story state is in `story/narrative_oriented_tree.json`.

## Examples

- To fetch a node: `GET /continue?node_id=<id>`
- To expand a node: `POST /expand` with `{ "parent_id": <id> }`
- To add a new word→child mapping, update the `options` field in the parent node and add the child to `children`.
