# File operations — brings all modules together

import json
import os

from models import Patient, EmergencyPatient, Doctor, PatientQueue
from utils import (
    logger, timer, validate_patient, require_records,
    patient_file, DataTransaction, generate_report, filter_high_risk, paginate, process_pipeline
)

DATA_FILE = "patients.json"

def save_patients(patients):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in patients], f, indent=2, ensure_ascii=False)
    print(f"\n[Record] {len(patients)} Patient record written to file. → {DATA_FILE}")

def load_patients():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return [Patient.from_dict(d) for d in json.load(f)]
    
@logger
@validate_patient
def register_patient(patient, queue):
    """Validates the patient and adds to the queue"""
    queue.add(patient)
    print(f"  ✅ {patient.name} added to queue.")

@timer
def run_report(patients):
    """Prints the report using a generator"""
    for line in generate_report(patients):
        print(line)

@require_records
def show_history(patient):
    """Displays the patient's medical history"""
    print(f"\n📋 Medical History: {patient.name}")
    for i, r in enumerate(patient.records, 1):
        print(f"  {i}. [{r['date']}] {r['note']}")

def main():
    print("=" * 55)
    print("   🏥  HEALTHTRACK — Clinic Management System")
    print("=" * 55)

    patients = [
        Patient("Alice Bob",  35, "P001", 70, 165),
        Patient("Bob Carol",  28, "P002", 95, 175),
        Patient("Carol David", 52, "P003", 55, 160),
        Patient("David Eve",  19, "P004", 45, 170),
        Patient("Eve Alice",  44, "P005", 85, 158),
        Patient("David Bob",  61, "P006", 72, 162),
    ]

    patients[0].add_record("Annual check-up - normal")
    patients[0].add_record("Blood pressure: 120/80")
    patients[0].add_medication("Vitamin D")

    patients[1].add_record("Obesity counseling")
    patients[1].add_medication("Metformin")
    patients[1].add_medication("Aspirin")

    patients[2].add_record("Osteoporosis screening")
    patients[2].add_record("Calcium deficiency was detected")
    patients[2].add_medication("Calcium")

    patients[4].add_record("Hypertension follow-up")
    patients[4].add_medication("Lisinopril")

    patients[5].add_record("Diabetes control")
    patients[5].add_medication("Insulin")

    doctor = Doctor("Martin Lion", 45, "D001", "Internal Medicine", "AB123456")
    for p in patients[:3]:
        doctor.assign_patient(p)

    emergency = EmergencyPatient("Karin Ozco", 67, "E001", 80, 172, "critical", "Chest pain")

    queue = PatientQueue()
    print("\n📥 Patients are being added to the queue:")
    for p in patients:
        register_patient(p, queue)

    print("\n" + "─" * 55)
    print("🔮 MAGIC METHODS")
    print(f"  str  :  {patients[0]}")   # __str__
    print(f"  repr : {repr(patients[1])}")  #__repr__
    print(f"  len  : {patients[0].name} → {len(patients[0])} Registration")   #__len__
    print(f"  bool : {patients[3].name} Is there a record? → {bool(patients[3])}")  # __bool__
    p_copy = Patient("Alice Bob", 35, "P001", 70, 165)
    print(f"  eq   : Alice == Copy of Alice → {patients[0] == p_copy}")  # __eq__
    print(f"  Acil : {emergency}")

    print("\n" + "─" * 55)
    print("👨‍⚕️  DOCTOR")
    print(f"  {doctor}")
    print(f"  Total doctor: {Doctor.get_doctor_count()}")
    print(f"  License valid: {Doctor.validate_license('AB123456')}")
    print(f"  Static BMI: {Patient.calculate_bmi(70, 165)}")

    print("\n" + "─" * 55)
    print(f"🔄 ITERATOR ─ {queue}" )
    for p in queue:
        print(f"  → {p.name} (Age: {p.age})")

    print("\n" + "─" * 55)
    print("📊 GENERATOR - Full Report:")
    run_report(patients)

    print("\n" + "─" * 55)
    print("🔴 GENERATOR - High-Risk Patients (BMI < 18.5 or ≥ 30)")
    high_risk = list(filter_high_risk(patients))
    if high_risk:
        for p in high_risk:
            print(f"  {p}")
    else:
        print("  No high-risk patients.")

    print("\n" + "─" * 55)
    print("📋 MAGIC METHOD - Sort by Age (__lt__):")
    for p in sorted(patients):
        print(f"  {p.age} age - {p.name}")

    print("\n" + "─" * 55)
    print("⚙️  GENERATOR PIPELINE - Age >= 30 and BMI <= 30:")
    for p in process_pipeline(patients, min_age=30, max_bmi=30):
        print(f"  {p}")

    print("\n" + "─" * 55)
    print("📄 GENERATOR - Pagination (3 per page)")
    for num, page in enumerate(paginate(patients, 3), 1):
        print(f"  Sayfa {num}: {[p.name for p in page]}")

    print("\n" + "─" * 55)
    print("📋 DECORATOR (@require_records) - Medical History:")
    try:
        show_history(patients[0])   # Record exists: active
        show_history(patients[3])   # No record: ValueError
    except ValueError as e:
        print(f"{e}")

    print("\n" + "─" * 55)
    print("💾 CONTEXT MANAGER - Transaction:")
    store = {p.id_number: p.name for p in patients}
    with DataTransaction(store) as data:
        data["TEMP"] = "Temporary Record"
        print(f" Added: {data["TEMP"]}")
    print(f"Number of records after operation: {len(store)}")

    print("\n" + "─" * 55)
    print("💾 CONTEXT MANAGER - Rollback (Error Scenario):")
    store2 = {"P001": "Alice"}
    with DataTransaction(store2) as data:
        data["P999"] = "Invalid Record"
        raise ValueError("Simulated error – rolling back!")
    print(f"After rollback: {store2}")

    print("\n" + "─" * 55)
    print("📁 CONTEXT MANAGER - File Operations:")
    save_patients(patients)
    loaded = load_patients()
    print(f" Number of patients uploaded: {len(loaded)}")
    print(f" First Uploaded: {loaded[0]}")

    print("\n" + "─" * 55)
    print("🏷️  PROPERTY - BMI Check:")
    for p in patients:
        print(f"  {p.name:15} BMI: {p.bmi:5} → {p.bmi_category}")

    print("\n" + "=" * 55)
    print("   ✅  20-Day Curriculum Project Completed!")
    print("=" * 55)

if __name__ == "__main__":
    main()


    






