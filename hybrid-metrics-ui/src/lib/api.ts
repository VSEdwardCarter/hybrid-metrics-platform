const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export type ThroughputMetric = {
    pipeline_name: string;
    records_processed: number;
    window_start: string;
    window_end: string;
    records_per_minute: number;
    measurement_window: string;
};

export type LateDataMetric = {
    pipeline_name: string;
    late_records: number;
    total_records: number;
    late_percentage: number;
    measurement_window: string;
};

export type QuarantineMetric = {
    pipeline_name: string;
    quarantined_records: number;
    reason_breakdown: Record<string, number>;
    measurement_window: string;
};

export type ApiResponse<T> = {
    data: T[];
};

async function fetchJson<T>(path: string): Promise<ApiResponse<T>> {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        cache: "no-store",
    });

    if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
}

export async function getTotalThroughput() {
    return fetchJson<ThroughputMetric>("/metrics/throughput");
}

export async function getCurrentThroughput() {
    return fetchJson<ThroughputMetric>("/metrics/current/throughput");
}

export async function getCurrentLateData() {
    return fetchJson<LateDataMetric>("/metrics/current/late-data");
}

export async function getCurrentQuarantine() {
    return fetchJson<QuarantineMetric>("/metrics/current/quarantine");
}