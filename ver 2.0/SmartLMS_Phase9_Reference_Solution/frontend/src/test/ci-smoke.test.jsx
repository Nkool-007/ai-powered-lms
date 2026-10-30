import {
  render,
  screen,
} from "@testing-library/react";

import {
  describe,
  expect,
  it,
} from "vitest";


function SmokeComponent() {
  return (
    <h1>
      SmartLMS
    </h1>
  );
}


describe(
  "SmartLMS frontend CI environment",
  () => {
    it(
      "runs React tests using Vitest and jsdom",
      () => {
        render(
          <SmokeComponent />
        );

        expect(
          screen.getByRole(
            "heading",
            {
              name: "SmartLMS",
            }
          )
        ).toBeInTheDocument();
      }
    );
  }
);
