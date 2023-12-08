function Stats({title, icon, value, description, colorIndex}){

    const COLORS = ["primary", "primary"]

    return(
        <div className="stats shadow">
            <div className="stat">
                <div className={`stat-figure dark:text-slate-300 text-${COLORS[colorIndex%2]}`}>{icon}</div>
                <div className="stat-title dark:text-slate-300">{title}</div>
                <div className={`stat-value dark:text-slate-300 text-${COLORS[colorIndex%2]}`}>{value}</div>
            </div>
        </div>
    )
}

export default Stats