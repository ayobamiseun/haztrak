import { screen } from '@testing-library/react';
import { RcraSiteType } from 'components/Manifest/manifestSchema';
import { SiteTypeSelect } from 'components/Manifest/SiteSelect/SiteTypeSelect';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { renderWithProviders } from 'test-utils';
import { describe, expect, test } from 'vitest';

function TestComponent({ siteType }: { siteType?: RcraSiteType }) {
  const [mockSiteType, setMockSiteType] = useState();
  const handleChange = (siteType: any) => setMockSiteType(siteType);
  const { control } = useForm();
  // @ts-ignore
  return (
    <SiteTypeSelect
      siteType={siteType}
      value={mockSiteType}
      handleChange={handleChange}
      control={control}
    />
  );
}

describe('SiteTypeSelect', () => {
  test('renders', () => {
    renderWithProviders(<TestComponent />);
    expect(screen.queryByTestId('siteTypeSelect')).toBeDefined();
  });
  test('site options are limited when site type is Generator', () => {
    renderWithProviders(<TestComponent siteType={'Generator'} />);
    // screen.debug(undefined, Infinity);
    expect(screen.queryByRole('option', { name: /generator/i })).toBeDefined();
    expect(screen.queryByRole('option', { name: /Transporter/i })).toBeNull();
    expect(screen.queryByRole('option', { name: /Tsdf/i })).toBeNull();
  });
  test('site options are limited when site type is transporter', () => {
    renderWithProviders(<TestComponent siteType={'Transporter'} />);
    // screen.debug(undefined, Infinity);
    expect(screen.queryByRole('option', { name: /generator/i })).toBeDefined();
    expect(screen.queryByRole('option', { name: /Transporter/i })).toBeDefined();
    expect(screen.queryByRole('option', { name: /Tsdf/i })).toBeNull();
  });
  test('All options are available when site Type is Tsdf', () => {
    renderWithProviders(<TestComponent siteType={'Tsdf'} />);
    // screen.debug(undefined, Infinity);
    expect(screen.queryByRole('option', { name: /generator/i })).toBeDefined();
    expect(screen.queryByRole('option', { name: /Transporter/i })).toBeDefined();
    expect(screen.queryByRole('option', { name: /Tsdf/i })).toBeDefined();
  });
  test('All options are available when site Type is undefined', () => {
    renderWithProviders(<TestComponent />);
    // screen.debug(undefined, Infinity);
    expect(screen.queryByRole('option', { name: /generator/i })).toBeDefined();
    expect(screen.queryByRole('option', { name: /Transporter/i })).toBeDefined();
    expect(screen.queryByRole('option', { name: /Tsdf/i })).toBeDefined();
  });
});
