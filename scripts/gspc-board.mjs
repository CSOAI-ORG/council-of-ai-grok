#!/usr/bin/env node
/**
 * Fetch the live GSPC board and print an honest summary.
 * Never fills UNMEASURED as 0. Fetch failure is UNREACHABLE, not a cached score.
 */
const ORIGIN = process.env.GSPC_ORIGIN || "https://councilof.ai";
const url = `${ORIGIN.replace(/\/$/, "")}/api/gspc`;

async function main() {
  let res;
  try {
    res = await fetch(url, { headers: { accept: "application/json" } });
  } catch (err) {
    console.log(`UNREACHABLE  could not fetch ${url}`);
    console.log(String(err && err.message ? err.message : err));
    process.exit(2);
  }
  if (!res.ok) {
    console.log(`UNREACHABLE  HTTP ${res.status} from ${url}`);
    process.exit(2);
  }
  const board = await res.json();
  const axes = Array.isArray(board.axes) ? board.axes : [];
  const totals = board.totals || {};
  console.log(`GSPC board  schema=${board.schema || "unknown"}`);
  console.log(`source      ${url}`);
  console.log(
    `totals      axes=${totals.axes ?? axes.length}  measured=${totals.measured_axes ?? "?"}  unmeasured=${totals.unmeasured_axes ?? "?"}`
  );
  const stamp =
    board.living_stamp ||
    (board.measured_on && board.measured_on.living_stamp) ||
    null;
  if (stamp) {
    console.log(
      `stamp       updated=${stamp.updated || "?"}  signed=${stamp.signed ?? "?"}  state=${stamp.verification_state || "?"}`
    );
  }
  console.log("");
  console.log("axis                      status        n     acc    sep          leader");
  console.log("-".repeat(88));
  for (const row of axes) {
    const status = String(row.status || row.kind || "?").toUpperCase();
    const unmeasured = status.includes("UNMEASURED");
    const n = unmeasured || row.n == null ? "—" : String(row.n);
    const acc =
      unmeasured || row.accuracy == null
        ? "—"
        : Number(row.accuracy).toFixed(3);
    const sep = row.separation || "—";
    const leader = row.leader || "—";
    const name = String(row.axis || row.name || "?").padEnd(24);
    console.log(`${name}  ${status.padEnd(12)}  ${n.padStart(4)}  ${acc.padStart(5)}  ${String(sep).padEnd(11)}  ${leader}`);
  }
  console.log("");
  console.log("Doctrine: MEASURED rows are evidence. UNMEASURED rows stay empty. Ties are not wins.");
  console.log("This is measurement, not certification. https://councilof.ai/verify");
}

main();
