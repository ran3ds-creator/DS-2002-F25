.PHONY: all fetch analyze clean
all: analyze

fetch:
	@echo "[fetch] Starting: fetching METAR data..."
	@./fetch_metars.sh
	@echo "[fetch] Finished: data saved in raw_metars/."

analyze: fetch
	@echo "[analyze] Starting: analyzing METAR data..."
	@./analyze_data.sh
	@echo "[analyze] Finished: weather_report.csv created."
	@echo "[pipeline] Pipeline completed successfully."

clean:
	@echo "[clean] Removing weather_report.csv and raw_metars/..."
	@rm -rf weather_report.csv raw_metars
	@echo "[clean] Workspace cleaned."
