import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "MarkMint";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          background: "#0A0A0A",
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          color: "#F3F0E8",
        }}
      >
        <div style={{ fontSize: 120, fontWeight: 900, letterSpacing: "-0.05em", display: "flex" }}>
          MarkMint
        </div>
        <div style={{ fontSize: 40, marginTop: 20, color: "#a1a1aa", display: "flex" }}>
          SRMIST AI & GPA Tracker
        </div>
      </div>
    ),
    { ...size }
  );
}
