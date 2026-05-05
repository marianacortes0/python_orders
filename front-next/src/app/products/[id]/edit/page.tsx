'use client';
import ProductForm from '../../../../components/forms/ProductForm';


export default function EditProductPage({ params }: { params: { id: string } }) {
  return <ProductForm id={params.id} />;
}
