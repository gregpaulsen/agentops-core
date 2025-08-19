"use client";
import { useRive } from "@rive-app/react-canvas";
export function Loader(){
  const { RiveComponent } = useRive({ src: "/rive/spinner.riv", autoplay: true });
  return <div style={{ width: 56, height: 56 }}><RiveComponent /></div>;
}


