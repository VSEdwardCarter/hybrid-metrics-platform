import MetricCard from "@/components/MetricCard";
import {
  getCurrentLateData,
  getCurrentQuarantine,
  getCurrentThroughput,
  getTotalThroughput,
} from "@/lib/api";

export default async function HomePage() {
  const [totalThroughput, currentThroughput, currentLateData, currentQuarantine] =
      await Promise.all([
        getTotalThroughput(),
        getCurrentThroughput(),
        getCurrentLateData(),
        getCurrentQuarantine(),
      ]);

  const totalThroughputMetric = totalThroughput.data[0];
  const currentThroughputMetric = currentThroughput.data[0];
  const currentLateMetric = currentLateData.data[0];
  const currentQuarantineMetric = currentQuarantine.data[0];

  return (
      <main className="min-h-screen bg-gray-50 px-6 py-10">
        <div className="mx-auto max-w-6xl">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Hybrid Metrics Dashboard</h1>
            <p className="mt-2 text-gray-600">
              Operational view of total and current pipeline metrics.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            <MetricCard
                title="Total Records Processed"
                value={totalThroughputMetric?.records_processed?.toLocaleString() ?? "N/A"}
                subtitle={totalThroughputMetric?.measurement_window ?? "Unavailable"}
            />

            <MetricCard
                title="Current Records Processed"
                value={currentThroughputMetric?.records_processed?.toLocaleString() ?? "N/A"}
                subtitle={currentThroughputMetric?.measurement_window ?? "Unavailable"}
            />

            <MetricCard
                title="Current Late Percentage"
                value={
                  currentLateMetric?.late_percentage !== undefined
                      ? `${currentLateMetric.late_percentage}%`
                      : "N/A"
                }
                subtitle={currentLateMetric?.measurement_window ?? "Unavailable"}
            />

            <MetricCard
                title="Current Quarantined Records"
                value={currentQuarantineMetric?.quarantined_records?.toLocaleString() ?? "N/A"}
                subtitle={currentQuarantineMetric?.measurement_window ?? "Unavailable"}
            />
          </div>

          <div className="mt-10 grid gap-6 md:grid-cols-2">
            <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-semibold text-gray-900">Total Throughput Details</h2>
              <div className="mt-4 space-y-2 text-sm text-gray-700">
                <p>
                  <span className="font-medium">Pipeline:</span>{" "}
                  {totalThroughputMetric?.pipeline_name ?? "N/A"}
                </p>
                <p>
                  <span className="font-medium">Window Start:</span>{" "}
                  {totalThroughputMetric?.window_start ?? "N/A"}
                </p>
                <p>
                  <span className="font-medium">Window End:</span>{" "}
                  {totalThroughputMetric?.window_end ?? "N/A"}
                </p>
                <p>
                  <span className="font-medium">Records/Minute:</span>{" "}
                  {totalThroughputMetric?.records_per_minute ?? "N/A"}
                </p>
              </div>
            </div>

            <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-semibold text-gray-900">Current Window Details</h2>
              <div className="mt-4 space-y-2 text-sm text-gray-700">
                <p>
                  <span className="font-medium">Pipeline:</span>{" "}
                  {currentThroughputMetric?.pipeline_name ?? "N/A"}
                </p>
                <p>
                  <span className="font-medium">Window Start:</span>{" "}
                  {currentThroughputMetric?.window_start ?? "N/A"}
                </p>
                <p>
                  <span className="font-medium">Window End:</span>{" "}
                  {currentThroughputMetric?.window_end ?? "N/A"}
                </p>
                <p>
                  <span className="font-medium">Records/Minute:</span>{" "}
                  {currentThroughputMetric?.records_per_minute ?? "N/A"}
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
  );
}