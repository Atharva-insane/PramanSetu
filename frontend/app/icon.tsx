import { ImageResponse } from "next/og";

export const size = {
  width: 32,
  height: 32,
};
export const contentType = "image/png";

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 20,
          background: "#0f2942",
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#ea580c",
          borderRadius: "6px",
          fontWeight: 900,
          border: "1px solid #ea580c",
        }}
      >
        प
      </div>
    ),
    {
      ...size,
    }
  );
}
