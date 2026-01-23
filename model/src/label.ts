export function getDefaultBlockLabel(data: {
  datasetLabel?: string;
  numPoints?: string;
  extrapolation: boolean;
}) {
  const parts: string[] = [];

  // Add dataset name if available
  if (data.datasetLabel) {
    parts.push(data.datasetLabel);
  }

  // Build secondary parts (points and extrapolation)
  const secondaryParts: string[] = [];
  if (data.numPoints) {
    secondaryParts.push(`${data.numPoints} points`);
  }
  if (data.extrapolation) {
    secondaryParts.push('extrapolated');
  }

  // Combine: "Dataset - 10 points, extrapolated"
  if (parts.length > 0 && secondaryParts.length > 0) {
    return `${parts[0]} - ${secondaryParts.join(', ')}`;
  } else if (secondaryParts.length > 0) {
    return secondaryParts.join(', ');
  } else if (parts.length > 0) {
    return parts[0];
  }

  return 'Select dataset';
}
