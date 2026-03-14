from langchain_core.tools import tool

FLIGHT_DATA = {
    "JQ101": {"status": "On time", "departure": "06:00", "arrival": "08:30", "route": "SYD → MEL"},
    "JQ202": {"status": "Delayed 90 minutes", "departure": "11:30", "arrival": "14:15", "route": "MEL → BNE"},
    "JQ303": {"status": "Cancelled", "departure": "N/A", "arrival": "N/A", "route": "SYD → DPS"},
    "JQ404": {"status": "On time", "departure": "14:45", "arrival": "17:00", "route": "BNE → SYD"},
}

PASSENGER_DATA = {
    "JS001": {"name": "Liam Chen", "tier": "Jetstar Plus", "credits": 12000},
    "JS002": {"name": "Priya Nair", "tier": "Standard", "credits": 800},
    "JS003": {"name": "Tom Walsh", "tier": "Jetstar Plus", "credits": 34000},
}

@tool
def get_flight_status(flight_number: str) -> str:
    """Get the current status of a Jetstar flight. Use this when the passenger asks about a specific flight status, departure time, arrival time, delay, or cancellation."""
    flight = flight_number.upper().strip()
    data = FLIGHT_DATA.get(flight)
    if not data:
        return f"No Jetstar flight found for '{flight}'. Please double-check the flight number."
    return f"Jetstar {flight} ({data['route']}): {data['status']}. Departure: {data['departure']} | Arrival: {data['arrival']}."

@tool
def get_rebooking_options(flight_number: str) -> str:
    """Get available rebooking options for a delayed or cancelled Jetstar flight. Use this when a passenger needs alternative flight options."""
    flight = flight_number.upper().strip()
    data = FLIGHT_DATA.get(flight)
    if not data:
        return f"No flight found for '{flight}'."
    if data["status"] == "On time":
        return f"Flight {flight} is currently on time. No rebooking required."
    return (
        f"Rebooking options for {flight} ({data['route']}):\n"
        f"  Option 1 — Tomorrow same route, 3 seats available\n"
        f"  Option 2 — Today 21:00, 1 seat remaining\n"
        f"  Option 3 — Full Jetstar travel credit refund\n"
        f"  Jetstar Plus members receive priority rebooking at no extra cost."
    )

@tool
def get_passenger_credits(passenger_id: str) -> str:
    """Get the Jetstar travel credits and membership tier for a passenger. Use this when a passenger asks about their credits, tier status, or membership benefits."""
    pid = passenger_id.upper().strip()
    passenger = PASSENGER_DATA.get(pid)
    if not passenger:
        return f"No passenger found with ID '{pid}'."
    tier = passenger["tier"]
    benefits = {
        "Jetstar Plus": "Priority boarding, free seat selection, 1 free checked bag, priority rebooking",
        "Standard": "Standard boarding, paid seat selection, carry-on only included",
    }
    return f"Passenger: {passenger['name']} | Tier: {tier} | Credits: {passenger['credits']:,} pts\nBenefits: {benefits[tier]}"

tools = [get_flight_status, get_rebooking_options, get_passenger_credits]
