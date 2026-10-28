# Data Quality Rules (Silver Layer)

This project uses synthetic automotive manufacturing data created solely for
learning and portfolio demonstration. It does not contain real data from any
company or production system.

## Principles

- Bronze keeps every source row unchanged. Silver applies the rules below.
- Valid rows go to Silver. Invalid rows go to quarantine with every failed
  rule ID and a plain-language reason. No row is dropped silently.
- A row can fail several rules; all failures are recorded.
- Reconciliation counts rows: Bronze = Silver + Quarantine + removed duplicates.
- Approved values come from `configs/reference_data.yaml` (single source of truth).
- Rules never "correct" values by guessing. Only standardization without
  guessing (for example trimming spaces) is allowed.
- Every rule was checked against the sample data for false positives before
  adoption.

## supplier_deliveries (prefix SD_)

| Rule ID | Row is rejected if | Reason |
|---|---|---|
| SD_ID_MISSING | delivery_id is NULL | Delivery ID is missing |
| SD_SUPPLIER_UNKNOWN | supplier_id NULL or not in supplier_ids | Supplier is not in the supplier master |
| SD_COMPONENT_UNKNOWN | component_id NULL or not in component_ids | Component is not in the component master |
| SD_PLANT_UNKNOWN | plant_id NULL or not in plant_ids | Plant is missing or unknown |
| SD_STATUS_INVALID | delivery_status NULL or not in delivery_statuses | Delivery status is not an approved value |
| SD_DATE_MISSING | planned or actual delivery date is NULL | Planned or actual delivery date is missing |
| SD_QTY_NEGATIVE | any quantity < 0 | A quantity is negative |
| SD_QTY_MISMATCH | accepted + rejected != delivered | Accepted plus rejected does not equal delivered |

## production_orders (prefix PO_)

| Rule ID | Row is rejected if | Reason |
|---|---|---|
| PO_ID_MISSING | production_order_id is NULL | Production order ID is missing |
| PO_MODEL_UNKNOWN | vehicle_model_id NULL or not in vehicle_model_ids | Vehicle model is missing or unknown |
| PO_PLANT_UNKNOWN | plant_id NULL or not in plant_ids | Plant is missing or unknown |
| PO_LINE_UNKNOWN | production_line_id NULL or not in production_line_ids | Production line is missing or unknown |
| PO_STATUS_INVALID | production_status NULL or not in production_statuses | Production status is missing or invalid |
| PO_TIME_MISSING | planned start/end NULL, or actual start/end NULL when status is COMPLETED | A required production time is missing |
| PO_TIME_ORDER | actual_end_time < actual_start_time | End date is before start date |
| PO_QTY_NEGATIVE | any of the four quantities < 0 | Quantity cannot be negative |
| PO_QTY_EXCEEDS_ACTUAL | rework_quantity + scrap_quantity > actual_quantity | Rework and scrap exceed actual quantity |

Producing less than planned is not a rule violation; it is measured by the
production target achievement KPI.

## quality_inspections (prefix QI_)

| Rule ID | Row is rejected if | Reason |
|---|---|---|
| QI_ID_MISSING | inspection_id is NULL | Inspection ID is missing |
| QI_VEHICLE_UNKNOWN | vehicle_id NULL or not in vehicle_ids | Vehicle is missing or unknown |
| QI_COMPONENT_UNKNOWN | component_id NULL or not in component_ids | Component is not in the component master |
| QI_SUPPLIER_UNKNOWN | supplier_id NULL or not in supplier_ids | Supplier is not in the supplier master |
| QI_PLANT_UNKNOWN | plant_id NULL or not in plant_ids | Plant is missing or unknown |
| QI_LINE_UNKNOWN | production_line_id NULL or not in production_line_ids | Production line is missing or unknown |
| QI_TIME_MISSING | inspection_timestamp is NULL | Inspection time is missing |
| QI_RESULT_INVALID | inspection_result NULL or not in inspection_results | Inspection result is not PASS or FAIL |
| QI_SEVERITY_INVALID | defect_severity not NULL and not in defect_severities | Defect severity is not an approved value |
| QI_DEFECT_CODE_INVALID | defect_code not NULL and not in defect_codes | Defect code is not an approved value |
| QI_PASS_HAS_DEFECT | result = PASS and defect_code or defect_severity not NULL | A passed inspection must have no defect details |
| QI_FAIL_MISSING_DEFECT | result = FAIL and defect_code or defect_severity is NULL | A failed inspection must have a defect code and severity |

## machine_downtime (prefix MD_)

| Rule ID | Row is rejected if | Reason |
|---|---|---|
| MD_ID_MISSING | downtime_event_id is NULL or blank | Downtime event ID is missing |
| MD_MACHINE_UNKNOWN | machine_id NULL or not in machine_ids | Machine is missing or not in the machine master |
| MD_LINE_UNKNOWN | production_line_id NULL or not in production_line_ids | Production line is missing or unknown |
| MD_REASON_INVALID | downtime_reason NULL or not in downtime_reasons | Downtime reason is missing or invalid |
| MD_FLAG_INVALID | planned_flag NULL or not in planned_flags | Planned flag is missing or invalid |
| MD_TIME_MISSING | start or end timestamp is NULL | Start or end time is missing |
| MD_TIME_ORDER | end_timestamp < start_timestamp | End date is before start date |
| MD_LOSS_NEGATIVE | production_loss_units < 0 | Production loss cannot be negative |
| MD_PLAN_MISMATCH | planned_flag contradicts the expected flag for the downtime reason | Planned flag contradicts the downtime reason |

## Design decisions

- **Date precision:** production and downtime times are currently dates only.
  Time-order rules therefore reject only end < start; equal dates are valid
  same-day events. With timestamps, rejecting equal times would be reviewed.
- **NULL handling:** list checks test NULL explicitly, because in Spark
  `NULL isin (...)` returns NULL instead of false.
- **Text flags:** planned_flag values are text ("True", "False") and are quoted
  in the YAML file so they are not parsed as booleans.

## Known source data issues (synthetic generator)

Found by data profiling; scheduled to be fixed in the generators:

- All valid deliveries have status LATE (no ON_TIME deliveries).
- About 48% of inspections fail, which is unrealistically high.
- Some scheduled-maintenance events have planned_flag "False";
  MD_PLAN_MISMATCH quarantines them.
- Downtime and production times have date precision only, so downtime
  duration in hours cannot be calculated yet.
