import { useState, useEffect } from "react";

const BUILDING_TYPE_OPTIONS = [
  "Events & Exhibits",
  "Library",
  "Hotel/Motel",
  "Office",
  "Restaurants",
  "Retail, Grocery",
  "School",
  "Warehouse",
  "Religious Worship",
  "Sports & Recreation",
  "Multifamily > 3 stories",
];

export default function PVCalculator() {
  const [cfa, setCfa] = useState(0);
  const [sara, setSara] = useState(0);
  const [numTypes, setNumTypes] = useState(1);
  const [buildingTypes, setBuildingTypes] = useState([{ type: "Office", proportion: 1 }]);
  const [zipcode, setZipcode] = useState("");
  const [efficiency, setEfficiency] = useState(0.9);
  const [climateData, setClimateData] = useState([]);
  const [output, setOutput] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/BuildingClimateZonesByZIPCode.json")
      .then((res) => res.json())
      .then((data) => setClimateData(data));
  }, []);

  const handleAddType = () => {
    setBuildingTypes([...buildingTypes, { type: "Office", proportion: 0 }]);
  };

  const handleTypeChange = (index, field, value) => {
    const updated = [...buildingTypes];
    updated[index][field] = field === "proportion" ? parseFloat(value) : value;
    setBuildingTypes(updated);
  };

  const handleSubmit = async () => {
    const matched = climateData.find(
      (entry) => entry["Zip Code"].toString() === zipcode
    );
    if (!matched) {
      setError("Invalid ZIP Code");
      return;
    }
    const climateZone = matched["Building CZ"];

    const totalProportion = buildingTypes.reduce((acc, bt) => acc + (bt.proportion || 0), 0);
    if (Math.abs(totalProportion - 1.0) > 0.01) {
      setError("Proportions must sum to 1. Currently: " + totalProportion.toFixed(2));
      return;
    }

    setError("");
    const result = {
      pv_kw: 12.34,
      bess_kwh: 45.6,
      bess_kw: 11.4,
    };
    setOutput(result);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-md py-4 px-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Green_leaf_icon.svg/512px-Green_leaf_icon.svg.png"
            alt="Company Logo"
            className="h-12 w-auto"
          />
          <h1 className="text-xl font-bold text-gray-800">Renewable Energy Solutions</h1>
        </div>
        <div className="text-sm text-gray-500 text-right">
          <p>Email: info@renewablesolutions.com</p>
          <p>Phone: (555) 123-4567</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="p-6 max-w-3xl mx-auto bg-white shadow-xl rounded-xl border border-blue-100 w-full mt-6">
        <h2 className="text-2xl font-bold text-blue-700 mb-6 border-b pb-2">PV & BESS Sizing Calculator</h2>

        <label className="block font-medium text-green-700">Conditioned Floor Area (ft²)</label>
        <input
          className="border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none rounded-md p-2 mb-4 w-full"
          type="number"
          value={cfa}
          onChange={(e) => setCfa(parseFloat(e.target.value))}
        />

        <label className="block font-medium text-green-700">SARA (ft²)</label>
        <input
          className="border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none rounded-md p-2 mb-4 w-full"
          type="number"
          value={sara}
          onChange={(e) => setSara(parseFloat(e.target.value))}
        />

        <label className="block font-medium text-green-700">ZIP Code</label>
        <input
          className="border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none rounded-md p-2 mb-4 w-full"
          type="text"
          value={zipcode}
          onChange={(e) => setZipcode(e.target.value)}
        />

        <label className="block font-medium text-green-700">BESS Round-Trip Efficiency (0–1)</label>
        <input
          className="border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none rounded-md p-2 mb-4 w-full"
          type="number"
          step="0.01"
          value={efficiency}
          onChange={(e) => setEfficiency(parseFloat(e.target.value))}
        />

        <h3 className="text-lg font-semibold text-blue-700 mt-6">Building Types</h3>
        {buildingTypes.map((bt, index) => (
          <div key={index} className="flex flex-col md:flex-row gap-4 mb-4">
            <div className="flex-1">
              <label className="block font-medium text-green-700">Type</label>
              <select
                className="border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none rounded-md p-2 w-full"
                value={bt.type}
                onChange={(e) => handleTypeChange(index, "type", e.target.value)}
              >
                {BUILDING_TYPE_OPTIONS.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>
            <div className="w-full md:w-40">
              <label className="block font-medium text-green-700">Proportion</label>
              <input
                className="border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none rounded-md p-2 w-full"
                type="number"
                step="0.01"
                placeholder="Proportion"
                value={bt.proportion}
                onChange={(e) => handleTypeChange(index, "proportion", e.target.value)}
              />
            </div>
          </div>
        ))}

        <button
          onClick={handleAddType}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md mb-6 transition-all"
        >
          + Add Building Type
        </button>

        {error && (
          <div className="mb-6 text-red-600 font-semibold bg-red-50 border border-red-200 rounded-md p-3">
            {error}
          </div>
        )}

        <button
          onClick={handleSubmit}
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-md w-full text-lg font-semibold transition-all"
        >
          Calculate
        </button>

        {output && (
          <div className="mt-8 p-6 border rounded-lg bg-gray-100 border-blue-200">
            <h4 className="font-bold text-blue-700 text-lg mb-3">Results</h4>
            <p className="mb-1"><strong>PV Size:</strong> {output.pv_kw.toFixed(2)} kWdc</p>
            <p className="mb-1"><strong>BESS Energy:</strong> {output.bess_kwh.toFixed(2)} kWh</p>
            <p><strong>BESS Power:</strong> {output.bess_kw.toFixed(2)} kW</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-auto py-4 text-center text-sm text-gray-500">
        &copy; {new Date().getFullYear()} Renewable Energy Solutions. All rights reserved.
      </footer>
    </div>
  );
}
