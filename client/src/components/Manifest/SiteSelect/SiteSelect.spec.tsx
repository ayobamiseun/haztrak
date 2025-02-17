import { screen } from '@testing-library/react';
import { SiteSelect } from 'components/Manifest/SiteSelect/SiteSelect';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { renderWithProviders } from 'test-utils';
import { createMockSite } from 'test-utils/fixtures';
import { createMockPermission } from 'test-utils/fixtures/mockHandler';
import { describe, expect, test } from 'vitest';

function TestComponent() {
  const [selected, setSelected] = useState();
  const { control } = useForm();
  // @ts-ignore
  return <SiteSelect value={selected} handleChange={setSelected} control={control} />;
}

describe('SiteSelect', () => {
  test('renders', () => {
    const mySite = createMockSite();
    renderWithProviders(<TestComponent />, {
      preloadedState: {
        rcraProfile: {
          user: 'username',
          phoneNumber: '1231231234',
          apiUser: false,
          rcraSites: {
            VATESTGEN001: {
              site: mySite,
              permissions: createMockPermission(),
            },
            VATEST00001: {
              site: mySite,
              permissions: createMockPermission(),
            },
          },
        },
      },
    });
    expect(screen.queryByTestId('siteSelect')).toBeDefined();
  });
});
