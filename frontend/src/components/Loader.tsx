export default function Loader({ label = "Generating PDF..." }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 text-govblue-700">
      <span className="h-5 w-5 border-2 border-govblue-300 border-t-govblue-700 rounded-full animate-spin" />
      <span className="text-sm font-medium">{label}</span>
    </div>
  );
}
