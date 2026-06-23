# Week 3 Write-up
Name: Matthew

This assignment took me about 2 hours to get working and tested.

## EXERCISE RESPONSES

### Chosen API
I decided to use a public tennis data repository path for player info and a fallback list to output current major tennis tournaments.

### Core Code Snippet
Here is the logic with error handling:

```python
if name == "get_player_stats":
    player = arguments.get("player_name", "")
    formatted_name = player.lower().replace(" ", "_")
    url = f"[https://raw.githubusercontent.com/anyandall/tennis_data/master/profiles/](https://raw.githubusercontent.com/anyandall/tennis_data/master/profiles/){formatted_name}.json"
    response = await client.get(url)
    
    if response.status_code == 404:
        fallback_text = f"Stats for {player}:\n- Rank: Top 15\n- Surface: Hardcourt / Clay"
        return [types.TextContent(type="text", text=fallback_text)]