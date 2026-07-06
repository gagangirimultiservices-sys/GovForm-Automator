export default function Header() {
  return (
    <header className="bg-govblue-900 text-white border-b-4 border-govgold-500 shadow-md">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-md bg-govgold-500 flex items-center justify-center font-bold text-govblue-900 text-lg">
            GMS
          </div>
          <div>
            <h1 className="text-lg font-bold leading-tight">GAGANGIRI MULTI SERVICES</h1>
            <p className="text-xs text-govblue-200 leading-tight">
              PAN CARD FORM  &middot; Form No. 93 (NEW PAN Application)
            </p>
          </div>
        </div>
        
      </div>
    </header>
  );
}
