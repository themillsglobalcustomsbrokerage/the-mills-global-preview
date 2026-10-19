# Image mapping

Which generated image feeds which website slot. Source files live in `assets/images/Mills Revamp Image Gen/` (not committed). Matched by file name against the prompts, then checked visually.

## Reused images (same picture in two slots)

- `Laboratory_equipment_in_cargo_se…`: cold-chain-07, healthcare-05

## Generated but not used (spares)

- `Cargo_in_port_warehouse`
- `Cargo_inspection_documents`
- `Logistics_worker_engaged_at_work`
- `Professionals_analyzing_map_at_desk`
- `Release_document_on_clipboard`
- `Trucks_operating_at_commercial_port`

## Notes

- Cutout slots (`*-cutout.png`) were background-removed with `tools/remove-bg.swift`; `time-critical-faq-cutout` (white paper on white) used a white-flood-fill instead.
- Most generated images are 16:9; portrait slots (split, cargo cards, floats) show a centered crop of them.
- `marine-faq-cutout` is small (293x458) because only the propeller was isolated.

## Slot to source

| Slot | Source image |
|---|---|
| `advisory-overview` | `Advisers_reviewing_regulatory_do…` |
| `advisory-cta-bg` | `City_skyline_viewed_through_window` |
| `advisory-faq-cutout` | `Professional_annotating_regulato…` |
| `advisory-why-split` | `Pen_on_agency_forms_stack` |
| `customs-overview` | `Customs_broker_reviewing_entry_d…` |
| `customs-cta-bg` | `Manila_port_container_yard_dawn` |
| `customs-faq-cutout` | `Commercial_invoice_and_calculator` |
| `customs-why-split` | `Release_document_on_clipboard` |
| `dangerous-goods-overview` | `Logistics_worker_checking_cargo` |
| `dangerous-goods-cta-bg` | `Chemical_storage_depot_corridor` |
| `dangerous-goods-faq-cutout` | `Industrial_drums_on_white_backgr…` |
| `dangerous-goods-why-split` | `Safety_data_sheet_binder_and` |
| `entry-overview` | `Professionals_analyzing_map_at_desk` |
| `entry-cta-bg` | `Manila_skyline_with_port_cranes` |
| `entry-faq-cutout` | `Brass_compass_on_paper_map` |
| `entry-why-split` | `Cardboard_cartons_and_logistics_…` |
| `insurance-overview` | `Insurance_adviser_reviewing_carg…` |
| `insurance-cta-bg` | `Container_ship_navigating_stormy…` |
| `insurance-faq-cutout` | `Policy_folder_on_desk` |
| `insurance-why-split` | `Surveyor_photographing_damaged_s…` |
| `logistics-overview` | `Truck_dispatcher_and_driver_revi…` |
| `logistics-cta-bg` | `Cargo_trucks_driving_on_highway` |
| `logistics-faq-cutout` | `Wooden_crate_on_flatbed_trailer` |
| `logistics-why-split` | `Warehouse_worker_scanning_cargo` |
| `marine-overview` | `Surveyor_checking_shipping_docum…` |
| `marine-cta-bg` | `Tugboats_working_in_commercial_h…` |
| `marine-faq-cutout` | `Ship_propeller_on_dry_dock` |
| `marine-why-split` | `Vessel_registration_papers_and_s…` |
| `packaging-overview` | `Technician_crating_industrial_ma…` |
| `packaging-cta-bg` | `Industrial_packaging_workshop_ti…` |
| `packaging-faq-cutout` | `Wooden_export_crate_on_pallet` |
| `packaging-why-split` | `Industrial_foam_wrapping_metal_c…` |
| `permits-overview` | `Compliance_adviser_stamping_regu…` |
| `permits-cta-bg` | `Quiet_office_corridor_with_filin…` |
| `permits-faq-cutout` | `Stack_of_approved_regulatory_doc…` |
| `permits-why-split` | `Compliance_folders_with_rubber_s…` |
| `projects-overview` | `Engineers_supervising_port_crane…` |
| `projects-cta-bg` | `Heavy-lift_cargo_operation_at_port` |
| `projects-faq-cutout` | `Crane_boom_lifting_steel_hook` |
| `projects-why-split` | `Industrial_cargo_on_transport_tr…` |
| `time-critical-overview` | `Courier_carrying_pouch_at_terminal` |
| `time-critical-cta-bg` | `Freighter_aircraft_loading_at_night` |
| `time-critical-faq-cutout` | `Stopwatch_resting_on_customs_doc…` |
| `time-critical-why-split` | `Pallet_loaded_into_cargo_aircraft` |
| `industry-agriculture-regulatory-bg` | `High-quality_corporate_photography._Wide_perspective` |
| `industry-agriculture-cutout` | `Inspector_examining_plant_with_m…` |
| `industry-automotive-regulatory-bg` | `Vehicles_parked_at_port_terminal` |
| `industry-automotive-cutout` | `Industrial_equipment_lashed_with…` |
| `industry-aviation-regulatory-bg` | `Aircraft_engine_in_hangar` |
| `industry-aviation-cutout` | `Aircraft_turbine_engine_in_cradle` |
| `industry-chemicals-regulatory-bg` | `Industrial_chemical_tank_farm` |
| `industry-chemicals-cutout` | `ISO_tank_container_on_port` |
| `industry-cold-chain-regulatory-bg` | `Refrigerated_shipping_containers…` |
| `industry-cold-chain-cutout` | `Temperature_data_logger_on_boxes` |
| `industry-construction-regulatory-bg` | `Cranes_at_commercial_constructio…` |
| `industry-construction-cutout` | `Structural_steel_on_transport_tr…` |
| `industry-data-centers-regulatory-bg` | `Server_racks_in_data_center` |
| `industry-data-centers-cutout` | `Unwrapping_server_rack_crate` |
| `industry-electronics-telecom-regulatory-bg` | `Telecommunications_tower_overloo…` |
| `industry-electronics-telecom-cutout` | `Network_equipment_stacked_on_pal…` |
| `industry-food-beverage-regulatory-bg` | `Food_distribution_warehouse_aisle` |
| `industry-food-beverage-cutout` | `Stretch-wrapping_beverage_pallets` |
| `industry-freight-forwarders-regulatory-bg` | `Freight_forwarding_terminal_with…` |
| `industry-freight-forwarders-cutout` | `Freight_operations_desk_displayi…` |
| `industry-healthcare-regulatory-bg` | `Pharmaceutical_warehouse_shelving` |
| `industry-healthcare-cutout` | `Medical_devices_in_sterile_packa…` |
| `industry-manufacturing-regulatory-bg` | `Factory_floor_with_industrial_ma…` |
| `industry-manufacturing-cutout` | `CNC_machine_in_shipping_crate` |
| `industry-marine-regulatory-bg` | `Commercial_vessels_docked_at_marina` |
| `industry-marine-cutout` | `Yacht_hull_on_transport_cradle` |
| `industry-mining-regulatory-bg` | `Industrial_haul_trucks_operating…` |
| `industry-mining-cutout` | `Industrial_mining_drill_bit_clos…` |
| `industry-renewable-energy-regulatory-bg` | `Solar_farm_and_wind_turbines` |
| `industry-renewable-energy-cutout` | `Solar_panels_on_transport_pallet` |
| `industry-retail-regulatory-bg` | `Parcels_moving_on_conveyor_belts` |
| `industry-retail-cutout` | `Cardboard_cartons_on_wooden_pallet` |
| `agriculture-01` | `Seeds_in_cargo_port` |
| `agriculture-02` | `Commercial_plant_cargo_at_port` |
| `agriculture-03` | `Fresh_produce_in_cargo_port` |
| `agriculture-04` | `Agricultural_grains_in_port_cargo` |
| `agriculture-05` | `Packaged_animal_feeds_as_cargo` |
| `agriculture-06` | `Transport_enclosures_for_live_an…` |
| `agriculture-07` | `Crated_animal_products_in_port` |
| `agriculture-08` | `Fish_transport_containers_in_port` |
| `agriculture-09` | `Frozen_seafood_cargo_at_port` |
| `agriculture-10` | `Commercial_meat_shipments_in_port` |
| `automotive-01` | `Commercial_vehicles_in_port_ware…` |
| `automotive-02` | `Commercial_trucks_at_port` |
| `automotive-03` | `Transport_buses_at_port` |
| `automotive-04` | `Industrial_forklifts_at_port` |
| `automotive-05` | `Construction_cranes_at_port` |
| `automotive-06` | `Earthmoving_equipment_at_port` |
| `automotive-07` | `Ambulances_in_port_warehouse` |
| `aviation-01` | `Aircraft_fuselage_sections_in_port` |
| `aviation-02` | `Commercial_jet_engines_in_port` |
| `aviation-03` | `Aircraft_parts_in_cargo_crates` |
| `aviation-04` | `Avionics_equipment_in_cargo_pack…` |
| `aviation-05` | `Airport_ground-support_equipment…` |
| `aviation-06` | `Aviation_parts_in_cargo_port` |
| `chemicals-01` | `Drums_of_industrial_chemicals` |
| `chemicals-02` | `Laboratory_reagents_in_port_ware…` |
| `chemicals-03` | `Solvents_in_transport_containers…` |
| `chemicals-04` | `Industrial_coatings_in_port_ware…` |
| `chemicals-05` | `Gas_cylinders_secured_for_transport` |
| `chemicals-06` | `Transport_containers_at_port` |
| `chemicals-07` | `Commercial_fuel_transport_logist…` |
| `chemicals-08` | `Controlled_materials_in_Philippi…` |
| `cold-chain-01` | `Frozen_food_pallets_in_warehouse` |
| `cold-chain-02` | `Meat_shipments_at_port_warehouse` |
| `cold-chain-03` | `Bulk_frozen_seafood_crates_in` |
| `cold-chain-04` | `Dairy_shipment_in_port` |
| `cold-chain-05` | `Insulated_pharmaceutical_pallets…` |
| `cold-chain-06` | `Vaccine_transport_coolers_in_port` |
| `cold-chain-07` | `Laboratory_equipment_in_cargo_se…` |
| `construction-01` | `Construction_cranes_in_port` |
| `construction-02` | `Excavators_secured_for_transport` |
| `construction-03` | `Dismantled_concrete_batching_pla…` |
| `construction-04` | `Pallets_of_building_materials_in…` |
| `construction-05` | `Steel_piping_and_rebar_cargo` |
| `construction-06` | `Industrial_cement_products_and_b…` |
| `construction-07` | `Industrial_generators_in_cargo_port` |
| `construction-08` | `Elevator_components_in_cargo_port` |
| `data-centers-01` | `Data_servers_in_cargo_port` |
| `data-centers-02` | `Server_racks_prepared_for_transport` |
| `data-centers-03` | `Network_switches_in_cargo_crates` |
| `data-centers-04` | `Data_storage_arrays_shipped` |
| `data-centers-05` | `Industrial_UPS_systems_in_port` |
| `data-centers-06` | `Industrial_server_backup_batteri…` |
| `data-centers-07` | `Data_center_generators_in_port` |
| `data-centers-08` | `HVAC_units_in_port_transit` |
| `data-centers-09` | `Electrical_transformers_in_port` |
| `data-centers-10` | `Industrial_cable_spools_in_port` |
| `data-centers-11` | `Data_center_security_equipment_i…` |
| `electronics-telecom-01` | `Telecommunications_equipment_in_…` |
| `electronics-telecom-02` | `Commercial_radios_in_shipping_ca…` |
| `electronics-telecom-03` | `Routers_secured_on_pallets` |
| `electronics-telecom-04` | `Bulk_shipments_of_phones_in` |
| `electronics-telecom-05` | `IoT_sensors_in_cargo_packaging` |
| `electronics-telecom-06` | `Pallets_of_computers_in_warehouse` |
| `electronics-telecom-07` | `Electronics_peripherals_in_distr…` |
| `electronics-telecom-08` | `Storage_devices_in_cargo_port` |
| `food-beverage-01` | `Pallets_of_processed_food_cargo` |
| `food-beverage-02` | `Bulk_shipments_of_commercial_bev…` |
| `food-beverage-03` | `Sacks_of_food_in_warehouse` |
| `food-beverage-04` | `Nutritional_supplements_at_cargo…` |
| `food-beverage-05` | `Chilled_goods_in_cold_storage` |
| `food-beverage-06` | `Secure_shipment_of_commercial_al…` |
| `food-beverage-07` | `Retail_merchandise_in_port_wareh…` |
| `freight-forwarders-01` | `Cargo_pallets_waiting_on_tarmac` |
| `freight-forwarders-02` | `Shipping_containers_in_port` |
| `freight-forwarders-03` | `Courier_parcels_in_cargo_port` |
| `freight-forwarders-04` | `Cargo_secured_on_trailer` |
| `freight-forwarders-05` | `Client_shipments_staged_in_port` |
| `healthcare-01` | `Medicines_in_secure_packaging_tr…` |
| `healthcare-02` | `Vaccine_coolers_in_warehouse` |
| `healthcare-03` | `Medical_devices_in_transit_crates` |
| `healthcare-04` | `Diagnostic_machines_on_transport…` |
| `healthcare-05` | `Laboratory_equipment_in_cargo_se…` |
| `healthcare-06` | `Healthcare_supplies_in_port_ware…` |
| `manufacturing-01` | `Industrial_equipment_in_cargo_port` |
| `manufacturing-02` | `CNC_machining_equipment_secured_…` |
| `manufacturing-03` | `Industrial_presses_in_port_wareh…` |
| `manufacturing-04` | `Industrial_boilers_in_transit` |
| `manufacturing-05` | `Industrial_pumps_on_transport_pa…` |
| `manufacturing-06` | `Compressors_in_crates_at_port` |
| `manufacturing-07` | `Industrial_conveyor_belt_systems…` |
| `manufacturing-08` | `Robotic_arms_in_shipping_crates` |
| `manufacturing-09` | `Industrial_tooling_in_Philippine…` |
| `marine-01` | `Luxury_yachts_for_ocean_transport` |
| `marine-02` | `Speedboats_on_transport_trailers` |
| `marine-03` | `Industrial_barges_in_port` |
| `marine-04` | `Tugboats_lifted_for_transport` |
| `marine-05` | `Landing_Craft_Tanks_in_port` |
| `marine-06` | `Marine_diesel_engines_in_port` |
| `marine-07` | `Commercial_navigation_equipment_…` |
| `marine-08` | `Marine_cranes_at_port` |
| `marine-09` | `Industrial_winches_and_vessel_sp…` |
| `mining-01` | `Mining_machinery_at_port` |
| `mining-02` | `Commercial_drilling_equipment_in…` |
| `mining-03` | `Mineral_processing_systems_in_port` |
| `mining-04` | `Secured_drums_in_transit_setting` |
| `mining-05` | `Explosives_cargo_in_port_warehouse` |
| `mining-06` | `Mineral_samples_at_port` |
| `renewable-energy-01` | `Solar_panels_on_pallets_in` |
| `renewable-energy-02` | `Solar_inverters_in_crates` |
| `renewable-energy-03` | `Battery_energy_storage_systems_i…` |
| `renewable-energy-04` | `Wind_turbine_blades_in_port` |
| `renewable-energy-05` | `Industrial_turbines_on_trailers` |
| `renewable-energy-06` | `Electrical_transformers_at_port` |
| `renewable-energy-07` | `Industrial_cable_spools_in_port` |
| `renewable-energy-08` | `Solar_mounting_and_electrical_sy…` |
| `retail-01` | `Boxed_commercial_apparel_in_port` |
| `retail-02` | `Appliances_in_cargo_port` |
| `retail-03` | `Pallets_of_electronics_in_warehouse` |
| `retail-04` | `Cosmetic_products_in_cargo_port` |
| `retail-05` | `Cartons_in_warehouse_setting` |
| `retail-06` | `Retail_toy_shipments_in_distribu…` |
| `retail-07` | `Commercial_cargo_in_port_warehouse` |
| `home-services-float-1` | `Close-up_of_commercial_cargo` |
| `home-services-float-2` | `Commercial_port_logistics_operation` |
| `home-why-float` | `Logistics_team_in_office` |
| `home-stats-bg` | `Commercial_port_and_cargo_ship` |
| `about-who-we-are` | `Team_collaborating_in_office` |
| `about-bg` | `Commercial_cargo_and_transport_r…` |
| `about-process-cutout` | `Shipping_container_on_white_back…` |
| `about-different-split` | `Logistics_worker_reviewing_tablet` |
| `contact-intro` | `Desk_featuring_shipment_paperwor…` |
| `book-a-call-band` | `Professional_wearing_headset_at_…` |
| `learning-band` | `Logistics_guides_and_documents_o…` |
| `blog-bg` | `Logistics_environment_photography` |
| `blog-post-featured` | `Logistics_scene_matching_article…` |
| `blog-post-bg` | `Commercial_logistics_environment…` |
| `industries-hub-bg` | `Industrial_ports_and_factories_p…` |
| `industries-hub-float-1` | `Industrial_cargo_operations_detail` |
| `industries-hub-float-2` | `Shipping_containers_and_customs_…` |


## Common Challenges section backgrounds

Each industry page's "Common Challenges" section uses its own full-width photo (`assets/images/challenges/<industry>.jpg`), different from that page's hero and Regulatory Focus backgrounds. Sourced from the original generated cargo images.

| Slot | Source |
|---|---|
| `challenges/agriculture` | `Agricultural_grains_in_port_cargo` |
| `challenges/automotive` | `Ambulances_in_port_warehouse` |
| `challenges/aviation` | `Aircraft_fuselage_sections_in_port` |
| `challenges/chemicals` | `Laboratory_reagents_in_port_ware…` |
| `challenges/cold-chain` | `Meat_shipments_at_port_warehouse` |
| `challenges/construction` | `Construction_cranes_in_port` |
| `challenges/data-centers` | `Data_servers_in_cargo_port` |
| `challenges/electronics-telecom` | `Storage_devices_in_cargo_port` |
| `challenges/food-beverage` | `Bulk_shipments_of_commercial_bev…` |
| `challenges/freight-forwarders` | `Shipping_containers_in_port` |
| `challenges/healthcare` | `Diagnostic_machines_on_transport…` |
| `challenges/manufacturing` | `Industrial_equipment_in_cargo_port` |
| `challenges/marine` | `Speedboats_on_transport_trailers` |
| `challenges/mining` | `Explosives_cargo_in_port_warehouse` |
| `challenges/renewable-energy` | `Wind_turbine_blades_in_port` |
| `challenges/retail` | `Commercial_cargo_in_port_warehouse` |
