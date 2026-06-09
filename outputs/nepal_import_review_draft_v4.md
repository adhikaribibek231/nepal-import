# Nepal Import Review Draft

## 1. Cover Note

This draft summarizes the extracted PDF text, extracted facts, NEPQA mapping, and detected source conflicts. It is not a final approval decision.

## 2. Key Review Finding
The provided documents appear to cover different inverter model families. The imported model must be confirmed before this draft can be treated as a reliable import review package.

## 3. Documents Reviewed

- 188_1115.txt
- DSS_GZES230100125901_combined-1.txt

## 4. Product Summary

The documents appear to describe grid-connected PV inverters, but not the same model family.

**Source A — CE-1P series**
- Source file: DSS_GZES230100125901_combined-1.txt
- Product type: Single phase inverter
- IP rating: IP67
- Models found:
  - CE-1P3001G-230-EU
  - CE-1P5001G-230-EU
  - CE-1P6001G-230-EU
  - CE-1P8001G-230-EU
  - CE-1P10001G-230-EU
  - CE-1P13001G-230-EU
  - CE-1P16001G-230-EU
  - CE-1P18001G-230-EU
  - CE-1P20001G-230-EU

**Source B — SUN G06P3 series**
- Source file: 188_1115.txt
- Product type: Grid-connected PV Inverter
- IP rating: IP65
- Models found:
  AM2 models:
  - SUN-3K-G06P3-EU-AM2
  - SUN-4K-G06P3-EU-AM2
  - SUN-5K-G06P3-EU-AM2
  - SUN-6K-G06P3-EU-AM2
  - SUN-7K-G06P3-EU-AM2
  - SUN-8K-G06P3-EU-AM2
  - SUN-9K-G06P3-EU-AM2
  - SUN-10K-G06P3-EU-AM2
  - SUN-12K-G06P3-EU-AM2
  - SUN-15K-G06P3-EU-AM2
  AM2-P1 models:
  - SUN-3K-G06P3-EU-AM2-P1
  - SUN-4K-G06P3-EU-AM2-P1
  - SUN-5K-G06P3-EU-AM2-P1
  - SUN-6K-G06P3-EU-AM2-P1
  - SUN-7K-G06P3-EU-AM2-P1
  - SUN-8K-G06P3-EU-AM2-P1
  - SUN-9K-G06P3-EU-AM2-P1
  - SUN-10K-G06P3-EU-AM2-P1
  - SUN-12K-G06P3-EU-AM2-P1
  - SUN-15K-G06P3-EU-AM2-P1

**Review note:** These appear to be different inverter families. The exact model being imported should be confirmed.

Full extracted model list is available in `outputs/extracted_facts.json`.

## 5. Manufacturer and Factory Information

**Manufacturer:**
- Zhejiang CHISAGE New Energy Technology Co., Ltd

**Factory:**
- NingBo Deye Inverter Technology Co., Ltd.

**Certificate holder:**
- NingBo Deye Inverter Technology Co., Ltd.

**Applicant:**
- Zhejiang CHISAGE New Energy Technology Co., Ltd

## 6. Standards and Test Evidence

**NEPQA-relevant standards found:**
- IEC 61727:2004
- IEC 62109-1:2010
- IEC 62116:2014

**Other referenced standards found:**
- IEC 17065:2012
- IEC 60309
- IEC 60364-1
- IEC 60364-5-54
- IEC 60417
- IEC 60529
- IEC 60664
- IEC 60664-1
- IEC 60707
- IEC 60755
- IEC 60990
- IEC 62020
- IEC 62109
- IEC 62852

**Certificate numbers:**
- PCS-24-1022

**Report numbers:**
- GZES230100125901

## 7. NEPQA Mapping Summary

- `evidence_found`: 7
- `missing`: 23
- `not_assessed`: 3

**Evidence found:**
- IEC 61727:2004 certificate/test evidence should be provided.
  Notes: Matched extracted field: standard
- IEC 62116:2014 islanding prevention test evidence should be provided.
  Notes: Matched extracted field: standard
- IEC 62109-1:2010 safety evidence should be provided.
  Notes: Matched extracted field: standard
- Ingress protection should be at least IP65 according to IEC 60529.
  Notes: Matched extracted field: ip_rating
- Inverter should have fan cooling or an appropriate heat sink to avoid excessive heating.
  Notes: Matched extracted field: cooling_method
- Inverter label should include manufacturer name.
  Notes: Matched extracted field: manufacturer
- Inverter label should include brand, model, and type.
  Notes: Matched extracted field: model_name

## 8. Conflict Summary

### manufacturer

- Status: `missing_in_one_source`
- Source A: Zhejiang CHISAGE New Energy Technology Co., Ltd
- Source B: Not found
- Issue: manufacturer was found in Source A but not in Source B.
- Decision: Needs confirmation if this affects the imported product identity.

### product_type

- Status: `conflict`
- Source A: Single phase inverter
- Source B: Grid-connected PV Inverter
- Issue: product_type differs between Source A and Source B.
- Decision: Needs confirmation if this affects the imported product identity.

### standard

- Status: `conflict`
- Source A: IEC 60309, IEC 60364-1, IEC 60364-5-54, IEC 60417, IEC 60529, IEC 60664, IEC 60664-1, IEC 60707, IEC 60755, IEC 60990, IEC 62020, IEC 62109, IEC 62109-1:2010, IEC 62852
- Source B: IEC 17065:2012, IEC 61727:2004, IEC 62116:2014
- Issue: standard differs between Source A and Source B.
- Decision: Needs confirmation if this affects the imported product identity.

### model_name

- Status: `conflict`
- Source A: CE-1P series models listed in Product Summary
- Source B: SUN G06P3 AM2 / AM2-P1 models listed in Product Summary
- Issue: model_name differs between Source A and Source B.
- Decision: Needs confirmation if this affects the imported product identity.

### ip_rating

- Status: `conflict`
- Source A: IP67
- Source B: IP65
- Issue: ip_rating differs between Source A and Source B.
- Decision: Needs confirmation if this affects the imported product identity.

## 9. Missing Information

- IEC 62891:2020 MPPT efficiency evidence should be provided.
  Notes: No extracted evidence found for field: standard
- IEC 62109-2:2011 inverter safety evidence should be provided.
  Notes: No extracted evidence found for field: standard
- Local importer should provide an agreement with the principal inverter manufacturer stating warranty period.
  Notes: No extracted evidence found for field: warranty
- Catalogue and technical datasheet of the PV inverter should be provided.
  Notes: No extracted evidence found for field: datasheet
- Rated AC output voltage should be 400+/-10% VAC three-phase or 230+/-10% VAC single-phase.
  Notes: No extracted evidence found for field: ac_output_voltage
- Output frequency should be 50Hz +/- 2.5%.
  Notes: No extracted evidence found for field: frequency
- MPPT input efficiency should be at least 95%.
  Notes: No extracted evidence found for field: mppt_efficiency
- Inverter efficiency should be at least 95% up to 5kVA and at least 97% above 5kVA for transformerless topology.
  Notes: No extracted evidence found for field: inverter_efficiency
- Euro efficiency should be at least 94% up to 5kVA and at least 96% above 5kVA for transformerless topology, with efficiency curve.
  Notes: No extracted evidence found for field: euro_efficiency
- Transformer topology inverter efficiency should be at least 90%.
  Notes: No extracted evidence found for field: inverter_efficiency
- No-load loss should be less than 0.5% of rated power for transformerless topology.
  Notes: No extracted evidence found for field: no_load_loss
- No-load loss should be less than 1.5% of rated power for transformer topology.
  Notes: No extracted evidence found for field: no_load_loss
- Total harmonic distortion should be less than 5% at full load.
  Notes: No extracted evidence found for field: thd
- Power factor should be greater than 0.99 at nominal power and adjustable from 0.8 leading to 0.8 lagging.
  Notes: No extracted evidence found for field: power_factor
- Inverter should have built-in meter and data logger for external user interface monitoring.
  Notes: No extracted evidence found for field: data_logger
- Inverter should include DC reverse polarity, grid fault, and lightning feeder protection.
  Notes: No extracted evidence found for field: protection_features
- Inverter should support automatic wake-up, synchronization, and shutdown.
  Notes: No extracted evidence found for field: automatic_operation
- PV inverter warranty should be at least 5 years.
  Notes: No extracted evidence found for field: warranty
- Inverter label should include rated power in Watt or VA.
  Notes: No extracted evidence found for field: rated_power
- Inverter label should include input and output voltage in Volt and frequency in Hz.
  Notes: No extracted evidence found for field: voltage_frequency_label
- Inverter label should include maximum input voltage.
  Notes: No extracted evidence found for field: max_input_voltage
- Inverter label should include MPPT voltage range.
  Notes: No extracted evidence found for field: mppt_voltage_range
- Inverter label should include serial number.
  Notes: No extracted evidence found for field: serial_number

**Missing in one source:**
- manufacturer: manufacturer was found in Source A but not in Source B.

## 10. Items Needing Confirmation

- Certification body or lab should be IECEE/IECRE listed with PV inverter testing scope.
  Notes: This item requires manual review or source verification.
- PV inverter should match grid voltage, frequency, phase angle, and phase sequence.
  Notes: This item requires manual review or source verification.
- THD, flicker, DC injection, voltage range, frequency range, power factor range, and anti-islanding should follow Nepal grid code.
  Notes: This item requires manual review or source verification.

**Source conflicts needing confirmation:**
- product_type: product_type differs between Source A and Source B.
- standard: standard differs between Source A and Source B.
- model_name: model_name differs between Source A and Source B.
- ip_rating: ip_rating differs between Source A and Source B.

## 11. Limitations

- This draft only summarizes existing extracted facts, NEPQA mappings, and conflict results.
- It does not verify certification body listing or scope on IECEE/IECRE websites.
- It does not decide whether the product is approved for import.
- Missing values may mean the information is absent, not extracted yet, or present in a format not currently handled.
- Conflicts should be confirmed with the importer, manufacturer, or original document issuer.
