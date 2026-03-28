type MetricCardProps = {
    title: string;
    value: string | number;
    subtitle?: string;
};

export default function MetricCard({ title, value, subtitle }: MetricCardProps) {
    return (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <div className="text-sm font-medium text-gray-500">{title}</div>
            <div className="mt-2 text-3xl font-semibold text-gray-900">{value}</div>
            {subtitle ? <div className="mt-2 text-sm text-gray-600">{subtitle}</div> : null}
        </div>
    );
}